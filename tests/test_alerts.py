from diffusion_dashboard.metrics.alerts import deployment_alert
def test_deployment_green():
    assert deployment_alert(30,5,95,0.5) == 'GREEN'

def test_deployment_amber_when_partial_thresholds_met():
    assert deployment_alert(35,6,90,1.0) == 'AMBER'
