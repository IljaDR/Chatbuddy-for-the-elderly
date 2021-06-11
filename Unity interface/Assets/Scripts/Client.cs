using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System;
using System.Text;

// Code from https://github.com/tom-weiland/tcp-udp-networking
public class Client : MonoBehaviour
{
    public static Client instance;
    public static int dataBufferSize = 1024;

    public string ip = "127.0.0.1";
    public int port = 10000;
    public int myId = 0;
    public TCP tcp;
    public FishManager fish;

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else if (instance != this)
        {
            Debug.Log("Instance already exists, destroying object!");
            Destroy(this);
        }
    }

    private void Start()
    {
        tcp = new TCP(fish);
        ConnectToServer();
    }

    public void ConnectToServer()
    {
        tcp.Connect();
    }

    public class TCP
    {
        public TcpClient socket;

        private NetworkStream stream;
        private Packet receivedData;
        private byte[] receiveBuffer;
        private FishManager fish;

        public TCP(FishManager fish)
        {
            this.fish = fish;
        }

        public void Connect()
        {
            socket = new TcpClient
            {
                ReceiveBufferSize = dataBufferSize,
                SendBufferSize = dataBufferSize
            };

            receiveBuffer = new byte[dataBufferSize];
            socket.BeginConnect(instance.ip, instance.port, ConnectCallback, socket);
        }

        private void ConnectCallback(IAsyncResult _result)
        {
            socket.EndConnect(_result);

            if (!socket.Connected)
            {
                return;
            }

            stream = socket.GetStream();

            receivedData = new Packet();

            stream.BeginRead(receiveBuffer, 0, dataBufferSize, ReceiveCallback, null);
        }

        public void SendData(Packet _packet)
        {
            try
            {
                if (socket != null)
                {
                    stream.BeginWrite(_packet.ToArray(), 0, _packet.Length(), null, null);
                }
            }
            catch (Exception _ex)
            {
                Debug.Log($"Error sending data to server via TCP: {_ex}");
            }
        }

        private void ReceiveCallback(IAsyncResult _result)
        {

            try
            {
                int _byteLength = stream.EndRead(_result);
                if (_byteLength <= 0)
                {
                    // TODO: disconnect
                    return;
                }

                byte[] _data = new byte[_byteLength];
                Array.Copy(receiveBuffer, _data, _byteLength);

                string emotion = Encoding.ASCII.GetString(receiveBuffer, 0, _byteLength);

                switch (emotion)
                {
                    case "anger":
                        fish.fishEmotion = FishManager.Emotion.anger;
                        break;
                    case "fear":
                        fish.fishEmotion = FishManager.Emotion.fear;
                        break;
                    case "sadness":
                        fish.fishEmotion = FishManager.Emotion.sadness;
                        break;
                    case "joy":
                        fish.fishEmotion = FishManager.Emotion.joy;
                        break;
                    case "neutral":
                        fish.fishEmotion = FishManager.Emotion.neutral;
                        break;
                    default:
                        Debug.Log("Failed to assign emotion");
                        break;
                }
                fish.emotionCountdown = 7;
                fish.countdownLength = 15;
                /*receivedData.Reset(HandleData(_data));*/
                stream.BeginRead(receiveBuffer, 0, dataBufferSize, ReceiveCallback, null);
            }
            catch
            {
                // TODO: disconnect
            }
        }
    }
}