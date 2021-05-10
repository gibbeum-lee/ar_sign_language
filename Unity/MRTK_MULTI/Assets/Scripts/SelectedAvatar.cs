using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SelectedAvatar : MonoBehaviour
{
    public GameObject ME1;
    public GameObject ME2;
    
    // Start is called before the first frame update
    void Start()
    {
        if (PlayerPrefs.GetInt("AvatarType") == 1)
        {
            ME1.SetActive(true);
        }
        else if (PlayerPrefs.GetInt("AvatarType") == 2)
        {
            ME2.SetActive(true);
        }
    }
}
