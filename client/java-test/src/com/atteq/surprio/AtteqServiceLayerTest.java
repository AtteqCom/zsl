package com.atteq.surprio;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.AtteqServiceLayerImpl;
import com.atteq.asl.ServiceCallException;
import com.atteq.asl.performers.Method;
import com.atteq.asl.performers.Resource;
import com.atteq.asl.performers.Resource.RequestType;
import com.atteq.asl.results.Error;
import com.atteq.asl.results.GenericResult;
import com.atteq.asl.results.GenericResultFactory;
import com.atteq.asl.results.JsonResultOrErrorTransformer;
import com.atteq.asl.results.JsonResultTransformer;
import com.atteq.asl.results.ResultOrError;
import com.atteq.asl.tasks.Task;

public class AtteqServiceLayerTest {

	@SuppressWarnings("unchecked")
	public static void main(String[] args) throws ServiceCallException {
		AtteqServiceLayerImpl asl = new AtteqServiceLayerImpl();
		asl.setServiceLayerUrl("http://localhost");
		Task t = new Task("test_task", null);

		GenericResultFactory<Object> rf = new GenericResultFactory<Object>();
		GenericResult<Object> r = asl.perform(t, new JsonResultTransformer<Object, GenericResult<Object>>(rf), Object.class);
		System.out.println(r.getResult());
		System.out.println(asl.perform(t, Object.class).getResult());

		Method m = new Method("test_method");
		System.out.println(asl.perform(m, Object.class).getResult());

		m = new Method("user/send_validation_code_by_phone_no", "00420608902447");
		GenericResultFactory<ResultOrError<Object, Error>> erf = new GenericResultFactory<ResultOrError<Object, Error>>();
		JsonResultOrErrorTransformer<Object, com.atteq.asl.results.Error> transformer = new JsonResultOrErrorTransformer<Object, Error>(erf);
		JavaType type = transformer.getType(Object.class, Error.class);
		Map<String, Object> mr;
		mr = (Map<String, Object>) asl.perform(m, transformer, type).getResult().getResult();
		String userId = mr.get("user_id").toString();
		String validationCode = ((Map<String, Object>) mr.get("validation_code")).get("code").toString();
		String validationId = ((Map<String, Object>) mr.get("validation_code")).get("id").toString();
		System.out.println(asl.perform(m, transformer, type).getResult().getResult());

		m = new Method("user/send_validation_code_by_phone_no", "420608902447");
		System.out.println(asl.perform(m, transformer, type).getResult().getError());

		String secretToken = asl.perform(new Method("user/create_secret_token", userId, validationId, validationCode), transformer, type).getResult()
				.getResult().toString();
		String authToken = ((Map<String, Object>) asl.perform(new Method("user/create_auth_token", userId, secretToken), transformer, type).getResult()
				.getResult()).get("token").toString();

		Resource rs = new Resource("user", RequestType.READ, null, null, "1", authToken);
		System.out.println(asl.perform(rs, Object.class).getResult());

		rs = new Resource("user", RequestType.READ, null, null, authToken);
		System.out.println(asl.perform(rs, Object.class).getResult());

		rs = new Resource("surprise", RequestType.READ, null, null, authToken);
		System.out.println(asl.perform(rs, Object.class).getResult());

		Map<String, Object> data;

		data = new HashMap<>();
		data.put("state", "new");
		data.put("created", new Date());
		rs = new Resource("surprise", RequestType.CREATE, data, null, authToken);
		System.out.println(asl.perform(rs, Object.class).getResult());

		data = new HashMap<>();
		Map<String, String> newSurpriseArgs = new HashMap<>();
		newSurpriseArgs.put("synchronization-log", "true");
		data.put("state", "new");
		data.put("created", new Date());
		rs = new Resource("surprise", RequestType.CREATE, data, newSurpriseArgs, authToken);
		System.out.println(asl.perform(rs, Object.class).getResult());
	}
}
