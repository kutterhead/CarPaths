using UnityEngine;

public class CollissionControl : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created

    public int checkActual;
    public int vueltas;
    public int nodos = 0;
    void Start()
    {
        checkActual = -1;
        vueltas = 0;
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
                if (checkActual>nodos-1)
                {
                    vueltas++;

                    checkActual = 0;
                }

            }
        }
    }
}
