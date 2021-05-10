using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Photon.Pun;
using Photon.Realtime;

public class PlayerSync : MonoBehaviourPun, IPunObservable
{
    private PhotonView pv;
    private Transform tr;
    private Transform camTr;

    private Vector3 currPos;
    private Quaternion currRot;


    // Start is called before the first frame update
    void Start()
    {
        tr = GetComponent<Transform>();
        pv = GetComponent<PhotonView>();
        camTr = Camera.main.transform;
    }

    // Update is called once per frame
    void Update()
    {
        if (pv.IsMine) //PhotonView가 자신일 경우
        {
            tr.SetPositionAndRotation(camTr.position, camTr.rotation);
        }
        else //PhtonView가 네트워크를 통해 들어온 유저일 경우
        {
            tr.SetPositionAndRotation(currPos, currRot);
        }
    }
    
    public void OnPhotonSerializeView(PhotonStream stream, PhotonMessageInfo info)
    {
        if (stream.IsWriting) //전송한 데이터
        {
            stream.SendNext(camTr.position);
            stream.SendNext(camTr.rotation);
        }
        else //수신받은 데이터
        {
            currPos = (Vector3)stream.ReceiveNext();
            currRot = (Quaternion)stream.ReceiveNext();
        }
    }
}
