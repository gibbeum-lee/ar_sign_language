// [GCT700] AR Project / Team 3
// UDP socket & Player Control

using UnityEngine;
using System;
using System.IO;
using System.Net;
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
	string message;

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
				message = text;

			} catch(Exception e) {
				print(e.ToString());
			}
		}
	}

	// make the player speech
	public void Talk(string message)
	{
		print ("Talking ... ");
		
		// 1. Google TTS communication & play the voice here (how to send this voice to the other peer, using PUN?)
		
		// set tte message
		SetTextToSpeech tts = new SetTextToSpeech();
		SetInput si = new SetInput();
		si.text = message;
		SetVoice sv = new SetVoice();
		sv.languageCode = "ko-KR";
		sv.name = "ko-KR-Standard-B";
		sv.ssmlGennder = "FEMALE";
		tts.voice = sv;
		SetAudioConfig sa = new SetAudioConfig();
		sa.audioEncoding = "LINEAR16";
		sa.speakingRate = 0.8f;
		sa.pitch = 0;
		sa.volumeGainDb = 0;
		tts.audioConfig = sa;

		// posting
		var str = TTSPost(tts);
		GetContent info = JsonUtility.FromJson<GetContent>(str);
		var bytes = Convert.FromBase64String(info.audioContent);
		var f = ConvertByteToFloat(bytes);
		AudioClip audioClip = AudioClip.Create("audioContent", f.Length, 1, 44100, false);
		audioClip.SetData(f, 0);
		AudioSource audioSource = FindObjectOfType<AudioSource>();
		audioSource.PlayOneShot(audioClip);


//		SpeechSound.Play(44100); // Play TTS Sound with a 1 second delay to match the animation


		// 2. Triggering of talking motion here
//		Player.GetComponent<Animator>().SetTrigger("Talk");
	}
	private static float[] ConvertByteToFloat(byte[] array) {
		float[] floatArr = new float[array.Length / 2];
		for (int i = 0; i < floatArr.Length; i++) {
			floatArr[i] = BitConverter.ToInt16(array, i * 2) / 32768.0f;
		}
		return floatArr;
	}

	// check for variable value, and make the Player Talk
	void Update () 
	{
		if(speech == true)
		{
			Talk (message);
			speech = false;
		}
	}

	public string TTSPost(object data) {
		string str = JsonUtility.ToJson(data);
		var bytes = System.Text.Encoding.UTF8.GetBytes(str); // string to byte

		// TTS settings
		HttpWebRequest request = (HttpWebRequest) WebRequest.Create("https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=AIzaSyBXuDtzffkvx0JFINFgO92I8aVvB4epKiQ");
		request.Method = "Post";
		request.ContentType = "application/json";
		request.ContentLength = bytes.Length;

		// Sending Request
		try {
			using (var stream = request.GetRequestStream()) {
				stream.Write(bytes, 0, bytes.Length);
				stream.Flush();
				stream.Close();
			}

			HttpWebResponse response = (HttpWebResponse) request.GetResponse();
			StreamReader reader = new StreamReader(response.GetResponseStream());
			string json = reader.ReadToEnd();

			return json;
		}
		catch (WebException e) {
			Debug.Log (e);
			return null;
		}
	}
}

// TTS JSON ================================
[System.Serializable]
public class SetTextToSpeech {
	public SetInput input;
	public SetVoice voice;
	public SetAudioConfig audioConfig;
}
[System.Serializable]
public class SetVoice {
	public string languageCode;
	public string name;
	public string ssmlGennder;
}
[System.Serializable]
public class SetInput {
	public string text;
}
[System.Serializable]
public class SetAudioConfig {
	public string audioEncoding;
	public float speakingRate;
	public int pitch;
	public int volumeGainDb;
}
[System.Serializable]
public class GetContent {
	public string audioContent; // string of base64
}
// ========================================