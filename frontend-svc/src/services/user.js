import API from "plugins/http-proxy/http-client";
import { all, takeEvery, call, put } from "redux-saga/effects";
import { getURL } from "utils/url";
import notification from "components/Notification";

function* register({ payload }) {
  try {
    yield put({
      type: "user/saveState",
      payload: {
        isLoading: true,
      },
    });
    let response = yield call(
      async () =>
        await API.post(getURL("user/register", "BACKEND"), {
          username: payload.username,
          password: payload.password,
          repassword: payload.repassword,
        }),
    );
    if (response.status === 200) {
      localStorage.setItem("username", payload.username);
      yield put({
        type: "user/saveState",
        payload: {
          isLoading: false,
        },
      });
      notification("success", response.data.message);
      window.location.href = "/";
    }
  } catch (error) {
    yield put({
      type: "user/saveState",
      payload: {
        isLoading: false,
      },
    });
    notification(
      "error",
      error.response.data?.message ? error.response.data.message : error.message,
    );
  }
}

function* login({ payload }) {
  try {
    yield put({
      type: "user/saveState",
      payload: {
        isLoading: true,
      },
    });
    let response = yield call(
      async () =>
        await API.post("user/login", {
          username: payload.username,
          password: payload.password,
        }),
    );
    if (response.status === 200) {
      localStorage.setItem("username", payload.username);
      yield put({
        type: "user/saveState",
        payload: {
          isLoading: false,
        },
      });
      notification("success", response.data.message);
      window.location.href = "/";
    }
  } catch (error) {
    yield put({
      type: "user/saveState",
      payload: {
        isLoading: false,
      },
    });
    notification(
      "error",
      error.response.data?.message ? error.response.data.message : error.message,
    );
  }
}

export default function* watchAll() {
  yield all([
    yield takeEvery("user/register", register),
    yield takeEvery("user/login", login),
  ]);
}
