'use strict';

var CheckinIn = angular.module('CheckinIn', ['ngMaterial', 'ngSanitize']);
CheckinIn.controller('CheckinInCtrl', function($scope, $mdDialog, $mdToast, $mdSidenav) {

  var endpoint = "wss://n0cy74ab.api.satori.com";
  var appKey = "CF1EDbdeFC3aC712Ac8cAB5bbdDF8fdB";
  var channelName = "channel1";
  var channelName2 = "channel2";
  var channelName3 = "channel3";
  var usersCheckinChannel;
  var elevatorChannel;
  var temperatureChannel;

  var elevatorStatuses = ['acknowledged', 'registered', 'assigned', 'being fixed', 'fixed', 'being served', 'served soon', 'served (call handling ends)', 'canceled (call handling ends)', 'reassigned']
  
  var usersInto = {
    '64:BC:0C:E8:6D:4D': {
      name: 'Sergei',
      img: 'http://res.cloudinary.com/ideation/image/upload/c_thumb,g_face,c_fill,r_max,h_90,w_90/ahd9omvdvwi7t7xljmmy.jpg'
    },
    'F0:DB:E2:F2:D4:59': {
      name: 'Artem',
      img: 'http://res.cloudinary.com/ideation/image/upload/c_thumb,g_face,c_fill,r_max,h_90,w_90/adhhipi1xt5irn22ysul.jpg'
    },
    '8C:1A:BF:CC:A9:35': {
      name: 'Iaroslav',
      img: 'http://res.cloudinary.com/ideation/image/upload/c_thumb,g_face,c_fill,r_max,h_90,w_90/tb6sxetaefrc5typs3oj.jpg'
    }
  }
  
  var client = new RTM(endpoint, appKey);
  client.on('enter-connected', function () {
    console.log('Connected to Satori RTM!');
    usersCheckinChannel = subscribe_to_user();
    elevatorChannel = subscribe_to_elevator();
    temperatureChannel = subscribe_to_temperature();
  });
  client.start();

  function subscribe_to_user() {
    var usersCheckin = client.subscribe(channelName, RTM.SubscriptionMode.SIMPLE);
    console.log('subscribeToUsers')
    usersCheckin.on('enter-subscribed', function () {
      console.log('Subscribed to: ' + usersCheckin.subscriptionId);
    });

    usersCheckin.on('rtm/subscription/data', function(pdu) {
      console.log('pdu', pdu.body.messages);
      $scope.checkedUser = usersInto[pdu.body.messages[0].user];
      console.log('asdf', $scope.checkedUser)
      $scope.$digest();
    });
  };
  
  function subscribe_to_temperature() {
    var temperature = client.subscribe(channelName3, RTM.SubscriptionMode.SIMPLE);
    console.log('temperature')
    temperature.on('enter-subscribed', function () {
      console.log('Subscribed to: ' + temperature.subscriptionId);
    });

    temperature.on('rtm/subscription/data', function(pdu) {
      console.log('pdu', pdu.body.messages[0]);
      $scope.room = pdu.body.messages[0];
      console.log($scope.room)
      $scope.$digest();
    });
  };
  
  function subscribe_to_elevator() {
    var elevatorsData = client.subscribe(channelName2, RTM.SubscriptionMode.SIMPLE);
    console.log('subscribeToElevators')
    elevatorsData.on('enter-subscribed', function () {
      console.log('Subscribed to: ' + elevatorsData.subscriptionId);
    });

    elevatorsData.on('rtm/subscription/data', function(pdu) {
      console.log('pdu', pdu.body.messages);
      $scope.elevator = {
        level: (pdu.body.messages[0].deckLevel - 3000) / 3000,
        status: elevatorStatuses[pdu.body.messages[0].callState]
      };
      $scope.$digest();
    });
  };
  
});
