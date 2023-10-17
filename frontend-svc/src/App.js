import Loading from "components/CircleLoading";
import Layout from "components/Layout";
import { React, useEffect } from "react";
import { connect } from "react-redux";
import { Route, Routes } from "react-router-dom";
import { getLocalStorage } from "utils/token";
import Chat from "./pages/Chat";
import Chatbot from "./pages/Chatbot";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Layout404 from "components/Layout/NotFoundLayout/Layout404";

const App = (props) => {
  const { account, dispatch } = props;
  const { username, isLoading } = account;
  const encodedUsername = getLocalStorage("user");

  useEffect(() => {
    window.addEventListener("storage", () => {
      if (!getLocalStorage("user") || !getLocalStorage("au") || !getLocalStorage("ur")) {
        dispatch({
          type: "account/getCurrentUserInfo",
          payload: {
            isNotRedicted: false,
          },
        });
      }
    });
    if (!username) {
      dispatch({
        type: "account/getCurrentUserInfo",
        payload: {
          isNotRedicted: true,
        },
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dispatch]);

  if (username) {
    return (
      <Routes>
        <Route path="/" element={
            <Layout username={username}>
              <Chat />
            </Layout>
          } 
        />
        <Route path="/t/:chatUser" element={
            <Layout username={username}>
              <Chat />
            </Layout>
          } 
        />
        <Route path="/chatbot" element={
            <Layout username={username}>
              <Chatbot />
            </Layout>
          } 
        />
        <Route path="*" element={
            <Layout username={username}>
              <Layout404 />
            </Layout>
          } 
        />
      </Routes>
    );
  } else if ((username === null && encodedUsername !== null) || isLoading === true) {
    return (
      <Routes>
        <Route
          path="*"
          element={
            <Loading isLoading={true} breadCrumb={[]}>
              <Login />
            </Loading>
          }
        />
      </Routes>
    );
  } else {
    return (
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Login />} />
      </Routes>
    );
  }
}

const mapStateToProps = (state) => ({
  account: state.account,
});

export default connect(mapStateToProps)(App);
