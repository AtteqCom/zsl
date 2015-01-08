<?php

abstract class Service {
	
	/**
	 * Constructor of inherited class is responsible for setting this attribute.
	 * 
	 * security settings:
	 * 
	 * @var string SECURITY_TOKEN - security token used in secured tasks
	 */
	protected $_security_config = array(
		'SECURITY_TOKEN' => null,
	);

	/**
	 * Has responsibility for calling task on Service Layer.
	 * 
	 * @param string $task_name - name of the task
	 * @param $task_data - input data for the task
	 * @return unprocessed result of call to Service Layer
	 */
	abstract protected function _inner_call($task_name, $task_data) {}

	/**
	 * Calls given task. Task data will be processed by TaskDecorator's given in
	 * $decorators array.
	 * 
	 * @param Task $task - task to be called
	 * @param array (of strings) $decorators - array of TaskDecorator / TaskResultDecorator
	 * 		subclass names
	 * @return result processed by TaskResultDecorator's given in $decorators array 
	 */
	function call(Task $task, $decorators = array()) {
		$call_task_result = $this->_call_task($task, $decorators);
		return $this->_process_call_task_result($call_task_result, $decorators); 
	}
	
	private function _call_task(Task $task, $decorators) {
		$task = $this->_apply_task_decorators($task, $decorators);
		
		$task_data = $task->get_data();
		$task_name = $task->get_name();
		
		return $this->_inner_call($task_name, $task_data);
	}
	
	private function _process_call_task_result($call_task_result, $decorators) {
		$task_result = new RawTaskResult($task, $call_task_result);
		return $this->_apply_task_result_decorators($task_result, $decorators);
	}

	private function _apply_task_decorators(Task $task, $decorators) {
		foreach ($decorators as $decorator) {
			if ($this->_is_subclass_or_same_class($decorator, 'TaskDecorator')) {
				$task = new $decorator($task);
			}
		}

		return $task;
	}
	
	private function _apply_task_result_decorators(TaskResult $task_result,
		$decorators) {
		
		foreach ($decorators as $decorator) {
			if ($this->_is_subclass_or_same_class($decorator, 'TaskResultDecorator')) {
				$task_result = new $decorator($task_result);
			}
		}

		return $task_result;
	}
	
	private function _is_subclass_or_same_class($tested_class_name, $class_name) {
		return $tested_class_name == $class_name || is_subclass_of(
			$tested_class_name, $class_name);
	}
}


class WebService extends Service {

	/**
	 * web service settings:
	 * 
	 * @var string SERVICE_LAYER_URL - url to service layer
	 */
	private $_web_config = array(
		'SERVICE_LAYER_URL' => null,
	);

	/**
	 * Constructor of WebService class
	 * 
	 * @param array $web_config - see documentation for WebService::$_web_config
	 * 		attribute
	 * @param array $security_config - see documentation for
	 * 		Service::$_security_config attribute
	 */
	function __construct($web_config, $security_config) {
		$this->_web_config = $web_config;
		$this->_security_config = $security_config;
	}

	protected function _inner_call($task_name, $task_data) {
		$task_data = $this->_convert_to_string($task_data);
		return $this->_send_request_to_service_layer($task_name, $task_data);
	}
	
	private function _send_request_to_service_layer($task_name, $task_data) {
		$task_url = $this->_get_task_url($task_name);
		return $this->_send_json_http_request($task_url, $task_data);
	}
	
	private function _get_task_url($task_name) {
		$service_layer_url = $this->_get_service_layer_url();
		
		return $service_layer_url . $task_name;
	}
	
	private function _get_service_layer_url() {
		if (is_null($this->_web_config['SERVICE_LAYER_URL'])) {
			// raise exception
		}

		return $this->_web_config['SERVICE_LAYER_URL'];
	}

	private function _convert_to_string($data) {
		if (is_null($data)) {
			$data = 'null';
		} else if (!is_string($data)) {
			$data = "$data";
		}
		
		return $data;
	}

	private function _send_json_http_request($url, $json_encoded_data) {
		$http_request = $this->_create_json_http_request($url, $json_encoded_data);
		$http_request->send();

		return $http_request->getResponseBody();
	}

	private function _create_json_http_request($url, $json_encoded_data) {
		$http_request = new HttpRequest($url, HTTP_METH_POST);
		$http_request->setRawPostData($json_encoded_data);
		$http_request->setHeaders(array('Content-Type' => 'application/json'));

		return $http_request;
	}
}
