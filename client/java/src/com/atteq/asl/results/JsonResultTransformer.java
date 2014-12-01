package com.atteq.asl.results;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.type.TypeFactory;
import org.codehaus.jackson.type.TypeReference;

import com.atteq.asl.performers.Performer;

public class JsonResultTransformer<T, R extends Result<T>> implements ResultTransformer<T, R> {

	protected ResultFactory<T, R> factory;

	public JsonResultTransformer(ResultFactory<T, R> factory) {
		this.factory = factory;
	}

	@Override
	public R transform(Performer performer, String result, int status) throws TransformationException {
		ObjectMapper mapper = new ObjectMapper();
		final DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		mapper.setDateFormat(df);
		TypeReference<T> tr = new TypeReference<T>() {
		};
		try {
			System.out.println(result);
			T r = mapper.readValue(result, TypeFactory.defaultInstance().constructType(tr));
			return factory.create(performer, r);
		} catch (Exception e) {
			throw new TransformationException(e);
		}
	}

}
