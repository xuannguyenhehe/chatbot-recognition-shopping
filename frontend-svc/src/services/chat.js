import API from "plugins/http-proxy/http-client";
import { all, takeEvery, call, put } from "redux-saga/effects";
import { getURL } from "utils/url";
import notification from "components/Notification";
import i18n from "i18n";


function* getAllChats({ payload }) {
  try {
    yield put({
      type: "chat/saveState",
      payload: {
        isLoading: true,
      },
    });
    let response = yield call(
      async () =>
        await API.get(getURL("chat", "ENTRYPOINT"), {
          params: {
            is_get_last_message: payload.is_get_last_message,
          },
        })
    );
    if (response.status === 200) {
      if (payload.is_get_last_message) {
        yield put({
          type: "chat/saveState",
          payload: {
            chats: response.data?.data?.map(chat => ({
              _id: chat.id,
              name: chat.sender === payload.username ? chat.receiver : chat.sender,
              last_message: chat.last_message,
              last_message_user: chat.last_message_user,
              is_contact: true,
              avatarImage: null,
            })),
            isLoading: false,
          },
        });
        notification("success", i18n.t("notify.successGetChat"));
      }
      if (!payload.is_get_last_message) {
        yield put({
          type: "chat/saveState",
          payload: {
            contacts: response.data?.data?.map(chat => ({
              _id: chat.id,
              name: chat.sender === payload.username ? chat.receiver : chat.sender,
              avatarImage: null,
            })),
            isLoading: false,
          },
        });
      }
    }
  } catch (error) {
    yield put({
      type: "chat/saveState",
      payload: {
        isLoading: false,
      },
    });
    notification(
      "error",
      error.response?.data?.message ? error.response?.data.message : error.message,
    );
  }
}

function* createNewChat({ payload }) {
  try {
    let response = yield call(
      async () =>
        await API.post(getURL("chat", "ENTRYPOINT"), {
          username: payload.receiver,
          current_entities: [],
        })
    );
    if (response.status === 200) {
      yield put({
        type: "chat/getAllChats",
        payload: {
          username: payload.sender,
          is_get_last_message: true,
        },
      });
      yield put({
        type: "message/getMessages",
        payload: {
          chatUser: payload.receiver,
        },
      });
    }
  } catch (error) {
    notification(
      "error",
      error.response.data?.message ? error.response.data.message : error.message,
    );
  }
}

export default function* watchAll() {
  yield all([
    yield takeEvery("chat/getAllChats", getAllChats),
    yield takeEvery("chat/createNewChat", createNewChat),
  ]);
}
