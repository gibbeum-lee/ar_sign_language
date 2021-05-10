using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SelectMe : MonoBehaviour
{
    public void Me_1()
    {
        PlayerPrefs.SetInt("AvatarType", 1);
        SceneManager.LoadScene("AndroidMaker");
    }

    public void Me_2()
    {
        PlayerPrefs.SetInt("AvatarType", 2);
        SceneManager.LoadScene("AndroidMaker");
    }
}
