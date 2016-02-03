package com.atteq.asl.results;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import com.atteq.asl.AtteqServiceLayerImpl;
import com.atteq.asl.performers.Performer;
import com.atteq.asl.utils.JsonHelper;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.TypeFactory;

public class JsonResultOrErrorTransformer<ResultType, ErrorType extends Error> implements
		ResultTransformer<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> {

	protected ResultFactory<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> factory;
	protected ObjectMapper mapper = JsonHelper.createMapper();

	public JsonResultOrErrorTransformer(
			ResultFactory<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> factory) {
		this.factory = factory;
	}

	public JavaType getType(Class<ResultType> resultClass, Class<ErrorType> errorClass) {
		return mapper.getTypeFactory().constructParametrizedType(ResultOrError.class, ResultOrError.class, resultClass, errorClass);
	}

	public TypeFactory getTypeFactory() {
		return mapper.getTypeFactory();
	}

	public JavaType getType(JavaType resultType, JavaType errorType) {
		return mapper.getTypeFactory().constructParametrizedType(ResultOrError.class, ResultOrError.class, resultType, errorType);
	}

	@Override
	public GenericResult<ResultOrError<ResultType, ErrorType>> transform(Performer performer, String result, int status,
			JavaType type) throws TransformationException {
		final DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		mapper.setDateFormat(df);
		try {
			ResultOrError<ResultType, ErrorType> r;

			if (status == AtteqServiceLayerImpl.HTTP_STATUS_CODE_OK) {
				ResultType rr = mapper.readValue(result, type.containedType(0));
				r = new ResultOrError<ResultType, ErrorType>(rr);
			} else {
				ErrorType error = mapper.readValue(result, type.containedType(1));
				r = new ResultOrError<ResultType, ErrorType>(error);
			}
			return factory.create(performer, r);
		} catch (Exception e) {
			throw new TransformationException(e);
		}
	}

}
