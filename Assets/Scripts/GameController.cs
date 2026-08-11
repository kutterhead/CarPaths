using Barmetler.RoadSystem.Util;
using System.Collections;
using UnityEngine;

public class GameController : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created

    public int vueltaActual;
    public int checkActual;

    public GameObject[] checkPoints;
    public CheckPoint[] checkScript;




    void Start()
    {
        checkActual = 0;
        vueltaActual = 0;
        //checkPoints = GameObject.FindGameObjectsWithTag("Check");
        //System.Array.Resize(ref checkScript, checkPoints.Length);

        //int j = 0;
        // for (int i = checkPoints.Length-1; i > -1; i--) 
        //{
        //        checkScript[j] = checkPoints[i].GetComponent<CheckPoint>();
        //        checkScript[j].index = j;
        //        j++;
        //}



    }

    
}
