<?php

/**
 * Usage example to express the idea of working with AtteqServiceLayer. 
 */


require_once 'atteq_service_layer.php';

use AtteqServiceLayer as ASL;

// create client
$web_config = array('SERVICE_LAYER_URL' => 'http://my.service.layer.url/task/');
$security_config = array('SECURITY_TOKEN' => 'my super secret secure token');

$web_client = new ASL\WebClient($web_client, $security_config);


// prepare task
// task data doesn't have to be array. It depends on task and
// TaskDecorators (see bellow) you use
$task = new RawTask('example/my_super_task', array(
	'motto' => 'hate haters',
	'frequency' => 'every day',
));

// call task with some decorators
//
// $task is decorated with given TaskDecorator's. TaskDecorator's are responsible
// for processing task data to suitable format (= format that is expected on
// service layer side). If you want to chain more TaskDecorator's together,
// simply put them in array (second parameter of WebClient::call() method)
// in desirable order.
//
// we get $task_result which is TaskResult instance "decorated" (in this case) with
// JsonTaskResultDecorator. TaskResultDecorator's are responsible for processing data
// we get as response to our "call task" request. If you want to chain more
// TaskDecorator's together, simply put them in array (second parameter of
// WebClient::call() method) in desirable order.
// 
$task_result = $web_client->call($task, ['SecuredTaskDecorator', 'JsonTaskDecorator',
	'JsonTaskResultDecorator']);

// to get result (of request to service layer) parsed with given TaskResultDecorator's
// simply call get_result() method
$result = $task_result->get_result();
