<?php

namespace AtteqServiceLayer;

require_once('task.php');
require_once('task_result.php');
require_once('decorators.php');
require_once('exceptions.php');

function _name_with_namespace($name) {
	return __NAMESPACE__ . "\\$name";
}

abstract class Client {

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
	 * @param string $task_data - input data for the task; data should be in
	 * 		string format
	 * @return result of call to Service Layer
	 */
	abstract protected function _inner_call($task_name, $task_data);

	/**
	 * Calls given task. Task data will be processed by TaskDecorator's given in
	 * $decorators array.
	 * 
	 * @param Task $task - task to be called
	 * @param array (of strings) $decorators - array of TaskDecorator / TaskResultDecorator
	 * 		subclass names
	 * @return TaskResult instance - result processed by TaskResultDecorator's 
	 * 		given in $decorators array 
	 */
	function call(Task $task, $decorators = array()) {
		$decorated_task = $this->_apply_task_decorators($task, $decorators);
		$call_result = $this->_call_task($decorated_task);
		
		return $this->_process_call_result($decorated_task, $call_result,
			$decorators); 
	}
	
	function get_secure_token() {
		if (\is_null($this->_security_config['SECURITY_TOKEN'])) {
			throw new ClientException('SECURITY_TOKEN is not configured.');
		}
		
		return $this->_security_config['SECURITY_TOKEN'];
	}
	
	private function _call_task(Task $task) {
		$task_data = $task->get_data();
		$task_name = $task->get_name();
		
		return $this->_inner_call($task_name, $task_data);
	}
	
	private function _process_call_result(Task $task, $call_result, $decorators) {
		$task_result = new RawTaskResult($task, $call_result);
		return $this->_apply_task_result_decorators($task_result, $decorators);
	}

	private function _apply_task_decorators(Task $task, $decorators) {
		foreach ($decorators as $decorator) {
			if ($this->_is_subclass_or_same_class(_name_with_namespace($decorator),
				_name_with_namespace('TaskDecorator'))) {

				$class_name = _name_with_namespace($decorator);
				$task = new $class_name($task);
				
				if (\method_exists($task, 'set_client')) {
					$task->set_client($this);
				}
			}
		}

		return $task;
	}
	
	private function _apply_task_result_decorators(TaskResult $task_result,
		$decorators) {
		
		foreach ($decorators as $decorator) {
			if ($this->_is_subclass_or_same_class(_name_with_namespace($decorator),
				_name_with_namespace('TaskResultDecorator'))) {
				
				$class_name = _name_with_namespace($decorator);
				$task_result = new $class_name($task_result);

			if (\method_exists($task_result, 'set_client')) {
					$task_result->set_client($this);
				}
			}
		}

		return $task_result;
	}
	
	private function _is_subclass_or_same_class($tested_class_name, $class_name) {
		return $tested_class_name == $class_name || is_subclass_of(
			$tested_class_name, $class_name);
	}
	
	/**
	 * Returns class name with namespace specified.
	 * @param string $class_name - name of class without namespace
	 */
	private function _get_full_class_name($class_name) {
		return __NAMESPACE__ . "\\$class_name";
	}
}

/**
 * Client for calling service layer through HTTP requests.
 * 
 * @author jankes
 */
class WebClient extends Client {

	/**
	 * web client settings:
	 * 
	 * @var string SERVICE_LAYER_URL - url to service layer
	 */
	private $_web_config = array(
		'SERVICE_LAYER_URL' => null,
	);

	/**
	 * Constructor of WebClient class
	 * 
	 * @param array $web_config - see documentation for WebClient::$_web_config
	 * 		attribute
	 * @param array $security_config - see documentation for
	 * 		Client::$_security_config attribute
	 */
	function __construct($web_config, $security_config = array()) {
		$this->_web_config = array_merge($this->_web_config, $web_config);
		$this->_security_config = array_merge($this->_security_config,
			$security_config);
	}

	function get_task_url($task_name) {
		$service_layer_url = $this->_get_service_layer_url();

		return $service_layer_url . $task_name;
	}
	
	protected function _inner_call($task_name, $task_data) {
		$task_url = $this->get_task_url($task_name);
		return $this->_send_json_http_request($task_url, $task_data);
	}

	private function _get_service_layer_url() {
		if (is_null($this->_web_config['SERVICE_LAYER_URL'])) {
			throw new WebClientException('SERVICE_LAYER_URL is not configured.');
		}

		return $this->_web_config['SERVICE_LAYER_URL'];
	}

	/**
	 * implementovane cez curl, pretoze novsia verzia (>= 2.0) pecl_http
	 * extension (trieda HttpRequest) sa vyrazne lisi a je nekompatibilna od
	 * starsich verzii 
	 */
	private function _send_json_http_request($url, $json_encoded_data) {
		$curl_handle = $this->_create_curl_handle_for_json_http_request($url,
			$json_encoded_data);

		return $this->_execute_curl($curl_handle);
	}

	private function _create_curl_handle_for_json_http_request($url,
		$json_encoded_data) {
		
		$curl_handle = \curl_init($url);
		
		\curl_setopt($curl_handle, CURLOPT_CUSTOMREQUEST, 'POST');
		\curl_setopt($curl_handle, CURLOPT_POSTFIELDS, $json_encoded_data);
		\curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, true);
		\curl_setopt($curl_handle, CURLOPT_HTTPHEADER, array(
			'Content-Type: application/json',
		));

		return $curl_handle;
	}
	
	private function _execute_curl($curl_handle) {
		$response = \curl_exec($curl_handle);
		\curl_close($curl_handle);
		
		return $response;
	}
}
