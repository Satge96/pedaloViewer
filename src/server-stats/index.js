'use strict';
const WebSocket = require('../../');

const express = require('express');
const path = require('path');
const { createServer } = require('http');
const {PythonShell} = require('python-shell')

const AWS = require('aws-sdk')
const AWSMqttClient = require('aws-mqtt/lib/NodeClient')
const publishMessage = require('aws-mqtt/lib/publishMessage')

const app = express();
app.use(express.static(path.join(__dirname, '/public')));

const server = createServer(app);
const wss = new WebSocket.Server({ server });


AWS.config.region = 'us-east-1' 
AWS.config.credentials = AWS.config.credentials
 
const client = new AWSMqttClient({
  region: AWS.config.region,
  credentials: AWS.config.credentials,
  endpoint: 'a1pf89jo51hxr3-ats.iot.us-east-1.amazonaws.com', // NOTE: get this value with `aws iot describe-endpoint`
  clientId: 'mqtt-client-' + (Math.floor((Math.random() * 100000) + 1)), // clientId to register with MQTT broker. Need to be unique per client
  will: {
    topic: 'WillMsg',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false
  } 
})
 
client.on('connect', () => {
	var updateTopic = '$aws/things/+/shadow/update' 
	var getAcceptedTopic = '$aws/things/+/shadow/get/accepted' 
	client.subscribe(updateTopic)
	console.log('Subsribing to ' + updateTopic)
	client.subscribe(getAcceptedTopic)
	console.log('Subsribing to ' + getAcceptedTopic)
	client.publish("presence/",'Hello from nodejs client'); 
})
		
wss.on('connection', function (ws) {
	console.log("webclient connected")
	// request shadows from all devices
	var devices = ["nrf-352656101498254", "nrf-352656100463176", "nrf-352656108602718", "nrf-352656106109229"];
	for (let device of devices) 
	{
		var topic = "$aws/things/" + device + "/shadow/get";
		var msg = "{}";
		client.publish(topic, msg); 
	}
	
	// send region data from file
	var fs = require('fs'),
    path = require('path'),    
    filePath = path.join(__dirname, 'region.kml');

	fs.readFile(filePath, {encoding: 'utf-8'}, function(err,data){
		if (!err) 
		{
			// replace none ascii characters as leaflet can't handle it!!!
			ws.send(JSON.stringify({'region':data.replace(/[^\x00-\x7F]/g, "")}))
		} 
		else 
		{
			console.log(err);
		}
	});
	
	// send saved track data
	let options = {
		mode: 'text',
		pythonOptions: ['-u'], // get print results in real-time
		args: []
	};

	// create kml file from coordinates
	PythonShell.run('kmlFromConsoleParam.py', options, function (err, results) {
		if (err) throw err;
		var msg = JSON.stringify({'track':results.join("")})
		ws.send(msg);
	});
	
	// client websocket message handler
	ws.on('message', function incoming(message) {
		console.log("Received =" + message);
		const data = JSON.parse(message);
		if(data.clearTrack)
		{
			// cleare track data stored in data.json file
			console.log('clear kml track');
			var fs = require('fs'),
			path = require('path'),    
			filePath = path.join(__dirname, 'data.json');
			fs.writeFile('data.json', '{}', function (err) {
				if (err) throw err;
			});
		}
		if(data.hasOwnProperty('rented'))
		{
			var thingName = data.name;
			const topic = "$aws/things/" + thingName + "/shadow/update";
			var state = data.rented;
			var msg = `{"state":{"desired":{"rented":${state}}}}`;
			client.publish(topic, msg); 
			console.log("Send message to mqtt: " + msg);
		}
	});
	
	// mqtt message handler
	client.on('message', (topic, message) => {
		try
		{
			console.log('received msg from mqtt client')
			console.log(topic, message.toString())
			var msg = message.toString()
			
			data = JSON.parse(msg)
			console.log(data)
			
			if(data.hasOwnProperty('state'))
			{				
				if(data.state.hasOwnProperty('reported'))
				{
					var thingName = topic.split("/")[2];
					var shadowData = `{"shadow":{"thingname": "${thingName}","reported":${JSON.stringify(data.state.reported)}}}`
					/* var shadowData = `{"shadow":{"thingname":"${thingName}"}}` */
					console.log(shadowData)
					ws.send(shadowData)
					
					
					//update kml track
					if(topic.endsWith("shadow/update"))
					{
						if(data.state.reported.hasOwnProperty('GPS'))
						{
							var longitude = data.state.reported.GPS.longitude.toString()
							var latitude = data.state.reported.GPS.latitude.toString()
							//var name = data.device.toString()
							var name = "Pedalo_Test_31_MAI"
							
							var kmlMsg = longitude + ':' + latitude + ':' + name
							
							var data = [kmlMsg]
							let options = {
								mode: 'text',
								pythonOptions: ['-u'], // get print results in real-time
								args: data
							};

							// create kml file from coordinates
							PythonShell.run('kmlFromConsoleParam.py', options, function (err, results) {
								if (err) throw err;
								var res = JSON.stringify({'track':results.join("")})
								ws.send(res);
							});
						}
					}
				}
			}
		}
		catch (e) 
		{
		   console.log(e)
		}
	})

	ws.on('close', function () {
		console.log('websocket closed');
	});
});

server.listen(8080, function () {
	console.log('Listening on http://localhost:8080');
});
