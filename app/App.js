import React from 'react';
import {
  StyleSheet,
  Text,
  Picker,
  Switch,
  View,
  Slider
} from 'react-native';

import {
  Button,
  List,
  Header,
  Icon,
  Avatar
} from 'react-native-elements'

import RTM from 'satori-rtm-sdk';

const SATORI_APPKEY = 'CF1EDbdeFC3aC712Ac8cAB5bbdDF8fdB'
const SATORI_ENDPOINT = 'wss://n0cy74ab.api.satori.com'

// create an RTM client instance
const rtm = new RTM(SATORI_ENDPOINT, SATORI_APPKEY);

// create a new subscription with "your-channel" name
const channel = rtm.subscribe('channel1', RTM.SubscriptionMode.SIMPLE);

const user = 'F0:DB:E2:F2:D4:59'

export default class App extends React.Component {
  
  constructor(props) {
    super(props);
    
    this.state = {
      chekedin: false,
      status: 'Aproach KONE elevator to check in',
      suite: '',
      temperature: 72,
      tv: '',
      color: '#fff',
      generalLight: false,
      bathroomLight: false
    };
        
    const onCheckIn = (data) => {
      this.setState({
        chekedin: true,
        status: 'You are checkedin',
        suite: data.suite_number
      })
    }
        
    // channel receives any published message
    channel.on("rtm/subscription/data", function(pdu) {
        pdu.body.messages.forEach((data) => {
          
          console.log(data);
          
          if ( user == data.user ) {            
            onCheckIn(data);
          }
        });
    });
    
    

    // client enters 'connected' state
    rtm.on("enter-connected", function() {
        // rtm.publish("your-channel", {key: "value"});
    });

    // client receives any PDU and PDU is passed as a parameter
    rtm.on("data", function(pdu) {
        if (pdu.action.endsWith("/error")) {
            rtm.restart();
        }
    });

    // start the client
    rtm.start();
  }
  
  onSetTemperature(temperature) {
    this.setState({temperature}, () => this.publishState())
  }
  
  onSetGeneralLight(generalLight) {
    this.setState({generalLight}, () => this.publishState())
  }
  
  onSetBathroomLight(bathroomLight) {
    this.setState({bathroomLight}, () => this.publishState())
  }
  
  publishState() {
    
    console.log(this.state);
    rtm.publish('channel3', {
        temperature: this.state.temperature,
        generalLight: this.state.generalLight,
        bathroomLight: this.state.bathroomLight,
        suite: this.state.suite,
        user: '8C:1A:BF:CC:A9:35'
      });
  }
  
  render() {
    
    return (
      <View style={styles.container}>
        <Header
          leftComponent={{ icon: 'menu' }}
          centerComponent={{ text: 'Welcome, Artem!' }}
          rightComponent={<Avatar
              small
              rounded
              source={{uri: "https://s.gravatar.com/avatar/781cb8fbb9362a3117a8bbdc447093ea"}}
              />}
          outerContainerStyles={styles.header}
        />
      <Text style={styles.large}>{this.state.status}</Text>
        
      <Icon
        name='tag-faces'
        iconStyle={{color: this.state.chekedin ? 'green' : '#ebebeb'}}
        size={200}
      />
      <View>
          <View>
            <Text style={styles.large}>Your room is {this.state.suite}</Text>
            <Text>Select Temperature</Text>  
              <Slider
              value={this.state.temperature} 
              maximumValue={90} 
              minimumValue={50} 
              maximumTrackTintColor={'red'}
              step={1}
              width={300}
              onValueChange={(temp) => this.onSetTemperature(temp)} />
            <Text>Value: {this.state.temperature}</Text>
          </View>
          <View style={styles.row}>  
            <Text style={styles.label}>General Light:</Text>
            <Switch
                value={this.state.generalLight}
                onValueChange={(value) => this.onSetGeneralLight(value)}/>
          </View>
          <View style={styles.row}>
            <Text style={styles.label}>Bathroom Light:</Text>
            <Switch
              value={this.state.bathroomLight}
              onValueChange={(value) => this.onSetBathroomLight(value)}/>
          </View>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  row: {
    marginTop: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  label: {
    paddingTop: 10
  },
  header: {
    marginTop: 20
  },
  container: {
    flex: 1,
    alignItems: 'stretch',
    justifyContent: 'center',
    backgroundColor: '#fff',
    alignItems: 'center',
    alignContent: 'center',
    justifyContent: 'center',
  },
  large: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10
  }
});
