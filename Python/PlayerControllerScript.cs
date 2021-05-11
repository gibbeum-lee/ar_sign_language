// [GCT700] AR Project / Team 3
// UDP socket & Player Control

using UnityEngine;
using System;
using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class PlayerControllerScript: MonoBehaviour
{
	// declare variables
	Thread receiveThread; // waiting thread
	UdpClient client; // will parse the predefined addr for data
	int PORT;

	public GameObject Player;
//	AudioSource SpeechSound;
	bool speech;

	// initialize variables
	void Start() 
	{
		PORT = 9999;
		speech = false;
//		SpeechSound = gameObject.GetComponent<AudioSource>();

		InitUDP();
	}

	// initUDP
	private void InitUDP()
	{
		print ("UDP Initialized");

		receiveThread = new Thread(new ThreadStart(ReceiveData));
		receiveThread.IsBackground = true;
		receiveThread.Start();
	}

	// receive Data
	private void ReceiveData()
	{
		client = new UdpClient(PORT); // create variable client
		while(true)
		{
			try
			{
				IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), PORT); // 0.0.0.0: any IP
				byte[] data = client.Receive(ref anyIP); // receive binary data from the endpoint
				string text = Encoding.UTF8.GetString(data); // binary to utf-8 string
				print ("Received >> " + text);

				speech = true;

			} catch(Exception e) {
				print(e.ToString());
			}
		}
	}

	// make the player speech
	public void Talk()
	{
		print ("Talking ... ");
		
		// Google TTS communication & play the voice here (how to send this voice to the other peer, using PUN?)



		// Triggering of talking motion here



//		Player.GetComponent<Animator>().SetTrigger("Talk");
//		SpeechSound.Play(44100); // Play TTS Sound with a 1 second delay to match the animation
	}

	// check for variable value, and make the Player Talk
	void Update () 
	{
		if(speech == true)
		{
			Talk ();
			speech = false;
		}
	}
}
