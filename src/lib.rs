use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::sync::Mutex;
use sysinfo::System;
use chrono::{DateTime, Utc};

/// Profiling metrics data structure
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ProfilingMetrics {
    pub start_time: DateTime<Utc>,
    pub end_time: Option<DateTime<Utc>>,
    pub duration_ms: Option<f64>,
    pub cpu_usage_percent: Option<f64>,
    pub memory_usage_mb: Option<f64>,
    pub memory_usage_percent: Option<f64>,
    pub request_id: String,
}

/// Global system monitor instance
static SYSTEM: Mutex<Option<System>> = Mutex::new(None);

/// TimeGlass Rust profiling engine
#[pymodule]
fn timeglass_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_profiling, m)?)?;
    m.add_function(wrap_pyfunction!(stop_profiling, m)?)?;
    m.add_function(wrap_pyfunction!(get_system_info, m)?)?;
    Ok(())
}

/// Initialize or refresh the system monitor
fn init_system_monitor() {
    let mut system_opt = SYSTEM.lock().unwrap();
    if system_opt.is_none() {
        let mut system = System::new_all();
        system.refresh_all();
        *system_opt = Some(system);
    } else if let Some(ref mut system) = *system_opt {
        system.refresh_all();
    }
}

/// Get current CPU usage percentage
fn get_cpu_usage() -> f64 {
    init_system_monitor();
    let system_opt = SYSTEM.lock().unwrap();
    if let Some(ref system) = *system_opt {
        system.global_cpu_usage() as f64
    } else {
        0.0
    }
}

/// Get current memory usage in MB and percentage
fn get_memory_usage() -> (f64, f64) {
    init_system_monitor();
    let system_opt = SYSTEM.lock().unwrap();
    if let Some(ref system) = *system_opt {
        let total_memory = system.total_memory() as f64;
        let used_memory = system.used_memory() as f64;
        let memory_mb = used_memory / 1024.0 / 1024.0;
        let memory_percent = if total_memory > 0.0 {
            (used_memory / total_memory) * 100.0
        } else {
            0.0
        };
        (memory_mb, memory_percent)
    } else {
        (0.0, 0.0)
    }
}

/// Start profiling for a request
#[pyfunction]
fn start_profiling(request_id: String) -> PyResult<String> {
    let start_time = Utc::now();
    let cpu_usage = get_cpu_usage();
    let (memory_mb, memory_percent) = get_memory_usage();

    let metrics = ProfilingMetrics {
        start_time,
        end_time: None,
        duration_ms: None,
        cpu_usage_percent: Some(cpu_usage),
        memory_usage_mb: Some(memory_mb),
        memory_usage_percent: Some(memory_percent),
        request_id: request_id.clone(),
    };

    // Store metrics in a simple in-memory map (in production, use a proper store)
    // For now, we'll serialize and return the initial metrics
    let json = serde_json::to_string(&metrics)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

    Ok(json)
}

/// Stop profiling and return metrics
#[pyfunction]
fn stop_profiling(_request_id: String, start_metrics_json: String) -> PyResult<String> {
    let end_time = Utc::now();
    let cpu_usage = get_cpu_usage();
    let (memory_mb, memory_percent) = get_memory_usage();

    // Parse the start metrics
    let mut metrics: ProfilingMetrics = serde_json::from_str(&start_metrics_json)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

    // Update with end metrics
    metrics.end_time = Some(end_time);
    metrics.duration_ms = Some((end_time - metrics.start_time).num_milliseconds() as f64);
    metrics.cpu_usage_percent = Some(cpu_usage);
    metrics.memory_usage_mb = Some(memory_mb);
    metrics.memory_usage_percent = Some(memory_percent);

    let json = serde_json::to_string(&metrics)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

    Ok(json)
}

/// Get basic system information
#[pyfunction]
fn get_system_info() -> PyResult<String> {
    init_system_monitor();
    let system_opt = SYSTEM.lock().unwrap();
    if let Some(ref system) = *system_opt {
        let info = serde_json::json!({
            "total_memory_mb": system.total_memory() / 1024 / 1024,
            "cpu_count": system.cpus().len(),
        });
        Ok(info.to_string())
    } else {
        Ok("{}".to_string())
    }
}
