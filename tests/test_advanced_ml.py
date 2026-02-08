"""
Tests for advanced ML/AI services.

Covers anomaly detection, trend forecasting, baseline optimization,
recommendation ranking, natural language alerts, retraining pipeline,
and explainability.
"""

import pytest
from datetime import datetime, timedelta


# =============================================================================
# Anomaly Detection Tests
# =============================================================================

class TestAnomalyDetection:

    def test_insufficient_data(self):
        from app.services.anomaly_detection import detect_anomalies
        result = detect_anomalies([{"heart_rate": 72}])
        assert result["status"] == "insufficient_data"
        assert result["anomaly_count"] == 0

    def test_empty_readings(self):
        from app.services.anomaly_detection import detect_anomalies
        result = detect_anomalies([])
        assert result["status"] == "insufficient_data"

    def test_no_anomalies_normal_data(self):
        from app.services.anomaly_detection import detect_anomalies
        readings = [{"heart_rate": 72, "spo2": 98} for _ in range(10)]
        result = detect_anomalies(readings)
        # All identical values means std=0, no z-score anomalies
        assert result["status"] == "normal"

    def test_detects_hr_zscore_anomaly(self):
        from app.services.anomaly_detection import detect_anomalies
        readings = [
            {"heart_rate": 72, "spo2": 98},
            {"heart_rate": 75, "spo2": 97},
            {"heart_rate": 73, "spo2": 98},
            {"heart_rate": 74, "spo2": 97},
            {"heart_rate": 71, "spo2": 98},
            {"heart_rate": 73, "spo2": 97},
            {"heart_rate": 180, "spo2": 97},  # HR anomaly
            {"heart_rate": 74, "spo2": 97},
            {"heart_rate": 72, "spo2": 98},
            {"heart_rate": 73, "spo2": 97},
        ]
        result = detect_anomalies(readings, z_threshold=2.0)
        assert result["status"] == "anomalies_detected"
        assert result["anomaly_count"] > 0
        hr_anomalies = [a for a in result["anomalies"] if a["metric"] == "heart_rate"]
        assert len(hr_anomalies) >= 1
        assert hr_anomalies[0]["direction"] == "high"

    def test_detects_spo2_anomaly(self):
        from app.services.anomaly_detection import detect_anomalies
        readings = [
            {"heart_rate": 72, "spo2": 98},
            {"heart_rate": 73, "spo2": 97},
            {"heart_rate": 72, "spo2": 98},
            {"heart_rate": 74, "spo2": 97},
            {"heart_rate": 71, "spo2": 98},
            {"heart_rate": 73, "spo2": 97},
            {"heart_rate": 72, "spo2": 82},  # SpO2 anomaly
            {"heart_rate": 73, "spo2": 98},
            {"heart_rate": 72, "spo2": 97},
            {"heart_rate": 74, "spo2": 98},
        ]
        result = detect_anomalies(readings, z_threshold=2.0)
        spo2_anomalies = [a for a in result["anomalies"] if a["metric"] == "spo2"]
        assert len(spo2_anomalies) >= 1

    def test_detects_hr_variability_spike(self):
        from app.services.anomaly_detection import detect_anomalies
        readings = [
            {"heart_rate": 72},
            {"heart_rate": 73},
            {"heart_rate": 130},  # 57 BPM jump (>40 threshold)
        ]
        result = detect_anomalies(readings)
        variability = [a for a in result["anomalies"] if a["metric"] == "hr_variability"]
        assert len(variability) >= 1

    def test_stats_returned(self):
        from app.services.anomaly_detection import detect_anomalies
        readings = [
            {"heart_rate": 70, "spo2": 97},
            {"heart_rate": 75, "spo2": 98},
            {"heart_rate": 80, "spo2": 96},
        ]
        result = detect_anomalies(readings)
        assert result["stats"]["hr_mean"] is not None
        assert result["stats"]["spo2_mean"] is not None


# =============================================================================
# Trend Forecasting Tests
# =============================================================================

class TestTrendForecasting:

    def test_insufficient_data(self):
        from app.services.trend_forecasting import forecast_trends
        result = forecast_trends([{"heart_rate": 72, "timestamp": "2026-01-01"}])
        assert result["status"] == "insufficient_data"

    def test_empty_data(self):
        from app.services.trend_forecasting import forecast_trends
        result = forecast_trends([])
        assert result["status"] == "insufficient_data"

    def test_increasing_hr_trend(self):
        from app.services.trend_forecasting import forecast_trends
        readings = []
        for i in range(14):
            readings.append({
                "heart_rate": 72 + i * 2,
                "spo2": 98,
                "timestamp": (datetime(2026, 1, 1) + timedelta(days=i)).isoformat()
            })
        result = forecast_trends(readings, forecast_days=14)
        assert result["status"] == "ok"
        assert result["trends"]["heart_rate"]["direction"] == "increasing"
        assert result["trends"]["heart_rate"]["slope_per_day"] > 0

    def test_stable_trend(self):
        from app.services.trend_forecasting import forecast_trends
        readings = []
        for i in range(14):
            readings.append({
                "heart_rate": 72,
                "timestamp": (datetime(2026, 1, 1) + timedelta(days=i)).isoformat()
            })
        result = forecast_trends(readings, forecast_days=14)
        assert result["status"] == "ok"
        assert result["trends"]["heart_rate"]["direction"] == "stable"

    def test_risk_projection(self):
        from app.services.trend_forecasting import forecast_trends
        readings = []
        for i in range(14):
            readings.append({
                "heart_rate": 72 + i * 2,
                "spo2": 98 - i * 0.3,  # decreasing SpO2
                "timestamp": (datetime(2026, 1, 1) + timedelta(days=i)).isoformat()
            })
        result = forecast_trends(readings, forecast_days=14)
        assert "risk_projection" in result
        assert "risk_direction" in result["risk_projection"]


# =============================================================================
# Baseline Optimization Tests
# =============================================================================

class TestBaselineOptimization:

    def test_insufficient_data(self):
        from app.services.baseline_optimization import compute_optimized_baseline
        result = compute_optimized_baseline([{"heart_rate": 72}])
        assert result["status"] == "insufficient_data"
        assert result["adjusted"] is False

    def test_computes_new_baseline(self):
        from app.services.baseline_optimization import compute_optimized_baseline
        readings = [{"heart_rate": hr} for hr in [68, 70, 72, 69, 71, 73, 68, 70]]
        result = compute_optimized_baseline(readings, current_baseline=80)
        assert result["status"] == "ok"
        assert result["new_baseline"] < 80  # Should adjust downward
        assert result["adjusted"] is True

    def test_no_change_when_matched(self):
        from app.services.baseline_optimization import compute_optimized_baseline
        readings = [{"heart_rate": hr} for hr in [70, 70, 70, 70, 70, 70]]
        result = compute_optimized_baseline(readings, current_baseline=70)
        assert result["new_baseline"] == 70
        assert result["adjusted"] is False

    def test_no_baseline_provided(self):
        from app.services.baseline_optimization import compute_optimized_baseline
        readings = [{"heart_rate": hr} for hr in [68, 70, 72, 69, 71, 73, 68]]
        result = compute_optimized_baseline(readings, current_baseline=None)
        assert result["status"] == "ok"
        assert result["new_baseline"] is not None

    def test_filters_out_of_range(self):
        from app.services.baseline_optimization import compute_optimized_baseline
        readings = [{"heart_rate": hr} for hr in [250, 250, 250, 250, 250]]  # All invalid
        result = compute_optimized_baseline(readings, current_baseline=70)
        assert result["status"] == "insufficient_valid_data"

    def test_confidence_increases_with_data(self):
        from app.services.baseline_optimization import compute_optimized_baseline
        small = [{"heart_rate": 70} for _ in range(5)]
        large = [{"heart_rate": 70} for _ in range(20)]
        r1 = compute_optimized_baseline(small, current_baseline=70)
        r2 = compute_optimized_baseline(large, current_baseline=70)
        assert r2["confidence"] >= r1["confidence"]


# =============================================================================
# Recommendation Ranking Tests
# =============================================================================

class TestRecommendationRanking:

    def test_deterministic_assignment(self):
        from app.services.recommendation_ranking import get_ranked_recommendation
        r1 = get_ranked_recommendation(user_id=42, risk_level="low")
        r2 = get_ranked_recommendation(user_id=42, risk_level="low")
        assert r1["variant"] == r2["variant"]

    def test_different_users_may_differ(self):
        from app.services.recommendation_ranking import get_ranked_recommendation
        variants = set()
        for uid in range(100):
            r = get_ranked_recommendation(user_id=uid, risk_level="low")
            variants.add(r["variant"])
        # With 100 users, should have both A and B
        assert len(variants) == 2

    def test_variant_override(self):
        from app.services.recommendation_ranking import get_ranked_recommendation
        r = get_ranked_recommendation(user_id=42, risk_level="low", variant_override="B")
        assert r["variant"] == "B"

    def test_high_risk_recommendation(self):
        from app.services.recommendation_ranking import get_ranked_recommendation
        r = get_ranked_recommendation(user_id=42, risk_level="high")
        assert r["risk_level"] == "high"
        assert "recommendation" in r

    def test_critical_maps_to_high(self):
        from app.services.recommendation_ranking import get_ranked_recommendation
        r = get_ranked_recommendation(user_id=42, risk_level="critical")
        assert r["risk_level"] == "high"

    def test_outcome_recording(self):
        from app.services.recommendation_ranking import record_recommendation_outcome
        result = record_recommendation_outcome(
            user_id=42, experiment_id="test_exp",
            variant="A", outcome="completed", outcome_value=0.3
        )
        assert result["status"] == "recorded"
        assert result["outcome"] == "completed"


# =============================================================================
# Natural Language Alerts Tests
# =============================================================================

class TestNaturalLanguageAlerts:

    def test_high_heart_rate_message(self):
        from app.services.natural_language_alerts import generate_natural_language_alert
        result = generate_natural_language_alert(
            alert_type="high_heart_rate", severity="critical",
            trigger_value="195 BPM", patient_name="Alice"
        )
        assert "Alice" in result["friendly_message"]
        assert "195 BPM" in result["friendly_message"]
        assert result["urgency_level"] == "urgent"
        assert len(result["action_steps"]) > 0

    def test_low_spo2_message(self):
        from app.services.natural_language_alerts import generate_natural_language_alert
        result = generate_natural_language_alert(
            alert_type="low_spo2", severity="critical",
            trigger_value="85%"
        )
        assert "oxygen" in result["friendly_message"].lower()
        assert result["urgency_level"] == "urgent"

    def test_with_risk_score(self):
        from app.services.natural_language_alerts import generate_natural_language_alert
        result = generate_natural_language_alert(
            alert_type="high_heart_rate", severity="warning",
            risk_score=0.85, risk_level="high"
        )
        assert result["risk_context"] is not None
        assert "elevated" in result["risk_context"].lower()

    def test_unknown_alert_type(self):
        from app.services.natural_language_alerts import generate_natural_language_alert
        result = generate_natural_language_alert(
            alert_type="unknown_type", severity="info"
        )
        assert result["friendly_message"] is not None
        assert result["urgency_level"] == "for_your_info"

    def test_risk_summary_formatting(self):
        from app.services.natural_language_alerts import format_risk_summary
        summary = format_risk_summary(
            risk_score=0.85, risk_level="high",
            drivers=["Peak heart rate exceeded safe limit (195 > 165)."],
            patient_name="Bob"
        )
        assert "Bob" in summary
        assert "concerning" in summary.lower()

    def test_risk_summary_low_risk(self):
        from app.services.natural_language_alerts import format_risk_summary
        summary = format_risk_summary(
            risk_score=0.2, risk_level="low",
            drivers=["Vitals are within expected safe limits."]
        )
        assert "good" in summary.lower()


# =============================================================================
# Retraining Pipeline Tests
# =============================================================================

class TestRetrainingPipeline:

    def test_readiness_not_enough_records(self):
        from app.services.retraining_pipeline import evaluate_retraining_readiness
        result = evaluate_retraining_readiness(new_records_count=50)
        assert result["ready"] is False

    def test_readiness_enough_records(self):
        from app.services.retraining_pipeline import evaluate_retraining_readiness
        result = evaluate_retraining_readiness(new_records_count=200)
        assert result["ready"] is True

    def test_readiness_too_recent(self):
        from app.services.retraining_pipeline import evaluate_retraining_readiness
        from datetime import datetime, timezone
        recent = datetime.now(timezone.utc).isoformat()
        result = evaluate_retraining_readiness(
            new_records_count=200, last_retrain_date=recent
        )
        assert result["ready"] is False

    def test_get_status(self):
        from app.services.retraining_pipeline import get_retraining_status
        status = get_retraining_status()
        assert status["model_exists"] is True
        assert "metadata" in status

    def test_prepare_training_data_valid(self):
        from app.services.retraining_pipeline import prepare_training_data
        records = [
            {"heart_rate": 72, "spo2": 98, "risk_label": "low"}
            for _ in range(60)
        ]
        result = prepare_training_data(records)
        assert result["status"] == "ok"
        assert result["valid_records"] == 60
        assert result["ready_for_training"] is True

    def test_prepare_training_data_empty(self):
        from app.services.retraining_pipeline import prepare_training_data
        result = prepare_training_data([])
        assert result["status"] == "no_data"

    def test_prepare_training_data_missing_fields(self):
        from app.services.retraining_pipeline import prepare_training_data
        records = [{"heart_rate": 72} for _ in range(10)]  # Missing spo2 and risk_label
        result = prepare_training_data(records)
        assert result["valid_records"] == 0
        assert result["skipped_records"] == 10


# =============================================================================
# Explainability Tests
# =============================================================================

class TestExplainability:

    def test_compute_feature_importance(self):
        from app.services.explainability import compute_feature_importance
        features = {
            "age": 65, "baseline_hr": 70, "max_safe_hr": 155,
            "avg_heart_rate": 120, "peak_heart_rate": 160,
            "min_heart_rate": 60, "avg_spo2": 93,
            "duration_minutes": 30, "recovery_time_minutes": 5,
            "hr_pct_of_max": 1.03, "hr_elevation": 50,
            "hr_range": 100, "duration_intensity": 30.9,
            "recovery_efficiency": 0.167, "spo2_deviation": 5,
            "age_risk_factor": 0.93, "activity_intensity": 2
        }
        columns = list(features.keys())
        result = compute_feature_importance(features, columns)
        assert len(result["top_features"]) <= 5
        assert result["method"] == "tree_importance_with_deviation_analysis"

    def test_explain_prediction(self):
        from app.services.explainability import explain_prediction
        prediction = {
            "risk_score": 0.75,
            "risk_level": "moderate",
            "features_used": {
                "age": 65, "baseline_hr": 70, "max_safe_hr": 155,
                "avg_heart_rate": 120, "peak_heart_rate": 160,
                "min_heart_rate": 60, "avg_spo2": 93,
                "duration_minutes": 30, "recovery_time_minutes": 5,
                "hr_pct_of_max": 1.03, "hr_elevation": 50,
                "hr_range": 100, "duration_intensity": 30.9,
                "recovery_efficiency": 0.167, "spo2_deviation": 5,
                "age_risk_factor": 0.93, "activity_intensity": 2
            }
        }
        columns = list(prediction["features_used"].keys())
        result = explain_prediction(prediction, columns)
        assert result["risk_score"] == 0.75
        assert "plain_explanation" in result
        assert "feature_importance" in result

    def test_explain_with_model(self):
        from app.services.explainability import explain_prediction
        from app.services.ml_prediction import load_ml_model, predict_risk
        from app.services.ml_prediction import model, feature_columns
        load_ml_model()
        pred = predict_risk(
            age=65, baseline_hr=70, max_safe_hr=155,
            avg_heart_rate=120, peak_heart_rate=130,
            min_heart_rate=68, avg_spo2=96,
            duration_minutes=30, recovery_time_minutes=5,
        )
        from app.services.ml_prediction import model as m, feature_columns as fc
        result = explain_prediction(pred, fc, m)
        assert result["risk_score"] == pred["risk_score"]
        assert len(result["feature_importance"]["global_importances"]) == 17
        top = result["feature_importance"]["top_features"]
        assert len(top) > 0
        assert "global_importance" in top[0]
