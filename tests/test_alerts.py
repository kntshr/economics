from diffusion_dashboard.metrics.alerts import deployment_alert
def test_deployment_green():
    assert deployment_alert(30,5,95,0.5) == 'GREEN'
