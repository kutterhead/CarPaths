using UnityEngine;

public class CollissionControl : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created

    public int checkActual;
    
    void Start()
    {
        checkActual = -1;
    }

    // Update is called once per frame
    void Update()
    {
        
    }


    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Check"))
        {
           if(other.gameObject.GetComponent<CheckPoint>().index> checkActual)
            {
                checkActual++;
            }
        }
    }
}
