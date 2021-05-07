using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Android;

public class CameraManager : MonoBehaviour
{
    WebCamTexture camTexture;
    public RawImage cameraViewImage; // 카메라가 보여질 화면

    public void CameraOn()
    {
        //카메라 권한 확인
        if (!Permission.HasUserAuthorizedPermission(Permission.Camera))
        {
            Permission.RequestUserPermission(Permission.Camera);
        }

        if(WebCamTexture.devices.Length == 0) //카메라가 없다면
        {
            Debug.Log("no camera!");
            return;
        }

        WebCamDevice[] devices = WebCamTexture.devices;
        int selectedCmaeraIndex = -1; 
        for(int i =0; i < devices.Length; i++) //전면카메라 찾기
        {
            if(devices[i].isFrontFacing == true)
            {
                selectedCmaeraIndex = i;
                break;
            }
        }

        if(selectedCmaeraIndex >= 0)
        {
            camTexture = new WebCamTexture(devices[selectedCmaeraIndex].name);
            camTexture.requestedFPS = 30; //카메라 프레임 설정
            cameraViewImage.texture = camTexture;
            camTexture.Play();
        }
    }
    public void CameraOff()
    {
        if(camTexture != null)
        {
            camTexture.Stop(); //카메라 정지
            WebCamTexture.Destroy(camTexture); //카메라 객체 삭제
            camTexture = null;
        }
    }
}

