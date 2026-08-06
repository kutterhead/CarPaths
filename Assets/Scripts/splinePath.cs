using UnityEngine;
using UnityEngine.Splines;

public class splinePath : MonoBehaviour
{
    public SplineContainer sp;

    [SerializeField] private GameObject knotPrefab;

    void Start()
    {
        if (sp == null || knotPrefab == null)
        {
            Debug.LogError("SplinePath necesita un SplineContainer y un prefab configurados.", this);
            return;
        }

        foreach (Spline spline in sp.Splines)
        {
            for (int i = 0; i < spline.Count; i++)
            {
                GameObject instance = Instantiate(knotPrefab, sp.transform);
                instance.transform.localPosition = spline[i].Position;
                instance.transform.localRotation = spline[i].Rotation;
            }
        }
    }
}
