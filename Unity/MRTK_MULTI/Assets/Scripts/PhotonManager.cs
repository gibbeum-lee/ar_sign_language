using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Photon.Pun;
using Photon.Realtime;
using System;

public class PhotonManager : MonoBehaviourPunCallbacks
{

    private const string version = "1.0";

    void Awake()
    {
        PhotonNetwork.AutomaticallySyncScene = true;
    }

    void Start()
    {
        PhotonNetwork.GameVersion = version;
        PhotonNetwork.ConnectUsingSettings();
    }

    public override void OnConnectedToMaster()
    {
        Debug.Log("Connected !!");
        PhotonNetwork.JoinRandomRoom();
    }

    public override void OnJoinRandomFailed(short returnCode, string message)
    {
        base.OnJoinRandomFailed(returnCode, message);
        RoomOptions ro = new RoomOptions();
        ro.IsOpen = true;
        ro.IsVisible = true;
        ro.MaxPlayers = 20;

        PhotonNetwork.CreateRoom("Room_001", ro); // 방 생성
    }

    public override void OnJoinedRoom() // 방 입장
    {
        base.OnJoinedRoom();

        Debug.Log("Entered Room!!");
        //아바타를 생성
        if (PlayerPrefs.GetInt("AvatarType") == 1)
        {
            PhotonNetwork.Instantiate("Me_1", Vector3.zero, Quaternion.identity, 0);
        }
        else if (PlayerPrefs.GetInt("AvatarType") == 2)
        {
            PhotonNetwork.Instantiate("Me_2", Vector3.zero, Quaternion.identity, 0);
        }
        //PhotonNetwork.Instantiate("Player", Vector3.zero, Quaternion.identity, 0);
    }
}
