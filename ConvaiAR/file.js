using UnityEngine;
using Vuforia;

public class ImageTargetHandler : MonoBehaviour
{
    public GameObject arContent; // The 3D model or content to display

    void Start()
    {
        VuforiaARController.Instance.RegisterVuforiaStartedCallback(OnVuforiaStarted);
    }

    private void OnVuforiaStarted()
    {
        var imageTargets = FindObjectsOfType<ImageTargetBehaviour>();
        foreach (var imageTarget in imageTargets)
        {
            imageTarget.RegisterOnTrackableStatusChanged(OnTrackableStatusChanged);
        }
    }

    private void OnTrackableStatusChanged(TrackableBehaviour.StatusChangeResult result)
    {
        if (result.NewStatus == TrackableBehaviour.Status.DETECTED ||
            result.NewStatus == TrackableBehaviour.Status.TRACKED)
        {
            arContent.SetActive(true); // Show content when target is detected
        }
        else
        {
            arContent.SetActive(false); // Hide content when target is lost
        }
    }

    void OnDestroy()
    {
        VuforiaARController.Instance.UnregisterVuforiaStartedCallback(OnVuforiaStarted);
    }
}
