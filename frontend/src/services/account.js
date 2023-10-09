import notification from "components/Notification";
import i18n from "i18n";
import API from "plugins/http-proxy/http-client";
import { all, call, put, takeEvery } from "redux-saga/effects";
import { Base64 } from "utils/base64";
import { getLocalStorage, removeLocalStorage, setLocalStorage } from "utils/token";
import { getURL } from "utils/url";

function* getCurrentUserInfo({ payload }) {
  try {
    yield put({
      type: "account/saveState",
      payload: {
        isLoading: true,
      },
    });
    let TOKEN_USER = getLocalStorage("au");
    let REFRESH_TOKEN_USER = getLocalStorage("ur");

    if (TOKEN_USER && REFRESH_TOKEN_USER) {
      let responseUserInfo = yield call(
        async () => await API.get(getURL("keycloak/user", "ENTRYPOINT")),
      );
      if (responseUserInfo.status === 200) {
        setLocalStorage("user", responseUserInfo.data.data.preferred_username);
        yield put({
          type: "account/saveState",
          payload: {
            idUser: responseUserInfo.data.data.sub,
            username: responseUserInfo.data.data.preferred_username,
            firstName: responseUserInfo.data.data.given_name,
            lastName: responseUserInfo.data.data.family_name,
            email: responseUserInfo.data.data.email,
            isLoading: false,
          },
        });
      }
    } else if (REFRESH_TOKEN_USER) {
      const bodyData = {
        refresh_token: REFRESH_TOKEN_USER,
      };
      const response = yield call(
        async () => await API.post(getURL("keycloak/token", "ENTRYPOINT"), bodyData),
      );
      if (response.status === 200) {
        yield put({
          type: "account/setCurrentUserInfo",
          payload: response.data,
        });
        yield put({
          type: "account/saveState",
          payload: {
            isLoading: false,
          },
        });
      }
    } else if (!payload?.isNotRedicted) {
      window.location.href = "/";
    } else {
      yield put({
        type: "account/saveState",
        payload: {
          isLoading: false,
        },
      });
    }
  } catch (error) {
    yield put({
      type: "account/saveState",
      payload: {
        isLoading: false,
      },
    });
    if (error.response?.status === 401) {
      notification("error", i18n.t("notify.errorLogin"));
    } else {
      notification(
        "error",
        error.response?.data?.error ? error.response.data.error : error.message,
      );
    }
  }
}

function* setCurrentUserInfo({ payload }) {
  try {
    const accessToken = payload.data.access_token;
    const refreshToken = payload.data.refresh_token;
    const parseAccessToken = Base64.parseJwt(accessToken);
    const parseRefreshToken = Base64.parseJwt(refreshToken);
    const expiresIn = parseAccessToken.exp;
    const refreshExpiresIn = parseRefreshToken.exp;
    setLocalStorage("au", accessToken, expiresIn);
    setLocalStorage("ur", refreshToken, refreshExpiresIn);
    setLocalStorage("user", payload.username);
    yield put({
      type: "account/getCurrentUserInfo",
    });
  } catch (error) {
    notification(
      "error",
      error.response?.data?.message ? error.response.data.message : error.message,
    );
  }
}

function* handleSignOut() {
  try {
    yield put({
      type: "account/saveState",
      payload: {
        isLoading: false,
      },
    });
    let responseLogout = yield call(
      async () => await API.post(getURL("keycloak/logout", "ENTRYPOINT")),
    );
    if (responseLogout.status === 200) {
      removeLocalStorage("au");
      removeLocalStorage("ur");
      removeLocalStorage("user");
      notification("success", i18n.t("notify.successLogout"));
      yield put({
        type: "account/saveState",
        payload: {
          idUser: null,
          belongedGroup: null,
          username: null,
          firstName: null,
          lastName: null,
          email: null,
          role: null,
          statusCode: responseLogout.status,
        },
      });
      yield put({
        type: "account/getCurrentUserInfo",
      });
      //redirect to login page
      const hostOrigin = window.location.origin;
      window.location.href = hostOrigin;
    }
  } catch (error) {
    notification(
      "error",
      error.response.data?.message ? error.response.data.message : error.message,
    );
  }
}

function* handleLogin({ payload }) {
  try {
    const response = yield call(
      async () => await API.post(getURL("keycloak/token", "ENTRYPOINT"), payload),
    );
    if (response.status === 200) {
      yield put({
        type: "account/setCurrentUserInfo",
        payload: {
          ...response.data,
          username: payload.username,
        },
      });
      yield put({ type: "account/handleLoginSuccess" });
      notification("success", i18n.t("notify.successLogin"));
    }
  } catch (error) {
    yield put({ type: "account/handleLoginFailure" });
    if (error.response?.status === 401) {
      notification("error", "Wrong username or password");
    } else
      notification(
        "error",
        error.response?.data?.message ? error.response.data.message : error.message,
      );
  }
}

export default function* watchAll() {
  yield all([
    yield takeEvery("account/getCurrentUserInfo", getCurrentUserInfo),
    yield takeEvery("account/setCurrentUserInfo", setCurrentUserInfo),
    yield takeEvery("account/handleSignOut", handleSignOut),
    yield takeEvery("account/handleLogin", handleLogin),
  ]);
}
