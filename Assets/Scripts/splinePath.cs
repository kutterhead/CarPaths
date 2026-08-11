using UnityEngine;
using UnityEngine.Splines;

public class splinePath : MonoBehaviour
{
    public SplineContainer sp;
    public CollissionControl cc;


    [SerializeField] private GameObject knotPrefab;
    public int nodos = 0;
    void Start()
    {
        if (sp == null || knotPrefab == null)
        {
            Debug.LogError("SplinePath necesita un SplineContainer y un prefab configurados.", this);
            return;
        }
        nodos = 0;
        foreach (Spline spline in sp.Splines)
        {
            nodos = spline.Count;
            cc.nodos = spline.Count;
            for (int i = 0; i < spline.Count; i++)
            {
                GameObject instance = Instantiate(knotPrefab, sp.transform);
                instance.transform.localPosition = spline[i].Position;
                instance.transform.localRotation = spline[i].Rotation;
                instance.GetComponent<CheckPoint>().index = i;


            }
        }
    }
}
