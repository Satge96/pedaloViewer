const AWS = require('aws-sdk')
const AWSMqttClient = require('aws-mqtt/lib/NodeClient')
const publishMessage = require('aws-mqtt/lib/publishMessage')
 
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
	var subTopic = '$aws/things/+/shadow/update' //'#' //'$aws/things'
	client.subscribe(subTopic)
	console.log('Subsribing to ' + subTopic)
	// publish returns a Promise
	// publishMessage(config, '/presence', 'Hello from nodejs client').then(console.log, console.error)
	client.publish("presence/",'Hello from nodejs client'); 
})
client.on('message', (topic, message) => {
  console.log(topic, message.toString('utf8'))
  data = JSON.parse(message)
  if(data.data == 'GPS')
  {
	  console.log('Longitude = ' + data.longitude.toString())
	  console.log('Latitude = ' + data.latitude.toString())
	  console.log('Devicename = ' + data.device.toString())
  }
})
client.on('close', () => {
  // ...
})
client.on('offline', () => {
  // ...
})
