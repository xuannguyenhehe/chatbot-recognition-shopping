import API from "plugins/http-proxy/http-client";
import { all, takeEvery, call, put, select } from "redux-saga/effects";
import { getURL } from "utils/url";

function* getMessages({ payload }) {
  try {
    yield put({
      type: "message/saveState",
      payload: {
        isShowLoading: true,
        messages: [],
      },
    });
    let response = yield call(
      async () =>
        await API.get(getURL("message", "ENTRYPOINT"), {
          params: {
            chat_id: payload.chatId,
          },
        }),
    );
    if (response.status === 200) {
      yield put({
        type: "message/saveState",
        payload: {
          messages: response.data.data.map((messageObj) => ({
            message: messageObj.message,
            image: messageObj.path_image
              ? process.env.REACT_APP_IMAGE_URL + messageObj.path_image
              : null,
            sender: messageObj.sender,
            receiver: messageObj.receiver,
          })),
          isShowLoading: false,
        },
      });
    }
  } catch (error) {
    yield put({
      type: "message/saveState",
      payload: {
        isShowLoading: false,
      },
    });
  }
}

function* sendMessage({ payload }) {
  const state = yield select();
  try {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: true,
      },
    });
    let body_image = null;
    if (payload.image) {
      body_image = {
        data: payload?.image.dataURL,
        filename: payload?.image.file.name,
      };
    }
    let body = {
      username: payload.username,
      chat_id: payload.chatId,
      message: {
        message: payload.message,
        is_from_self: true,
        image: body_image,
      },
    };
    let response = yield call(
      async () => await API.post(getURL("message", "BACKEND"), body),
    );
    if (response.status === 200) {
      let messages = [...state.message.messages];
      if (response.data?.data?.length > 0) {
        response.data.data.forEach((messageObj) => {
          messages.push({
            fromSelf: messageObj.is_from_self,
            message: messageObj.message,
            image: messageObj.path_image
              ? process.env.REACT_APP_IMAGE_URL + messageObj.path_image
              : null,
          });
        });
      }
      yield put({
        type: "message/saveState",
        payload: {
          messages: messages,
          isLoading: false,
        },
      });
    }
  } catch (error) {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: false,
      },
    });
  }
}

export default function* watchAll() {
  yield all([
    yield takeEvery("message/getMessages", getMessages),
    yield takeEvery("message/sendMessage", sendMessage),
  ]);
}
