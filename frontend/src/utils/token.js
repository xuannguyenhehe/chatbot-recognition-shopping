import { Base64 } from "utils/base64";

export function setCookie(cname, cvalue, seconds) {
  const d = new Date();
  d.setTime(d.getTime() + seconds * 1000);
  let expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

export function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

export function removeCookie(cname) {
  document.cookie = cname + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}

export function removeLocalStorage(keyname) {
  localStorage.removeItem(keyname);
}

export function setLocalStorage(key, value, seconds = 0) {
  if (!seconds) {
    const now = new Date();
    const item = {
      value: value,
      exp: now.getTime() + seconds * 1000,
    };
    localStorage.setItem(key, Base64.encode(JSON.stringify(item)));
  }
  else {
    localStorage.setItem(key, Base64.encode(value));
  }
}

export function getLocalStorage(key) {
  const value = localStorage.getItem(key);
  if (!value) {
    return null;
  }
  const now = new Date();
  let token = Base64.decode(value);
  if (token.exp) {
    if (now.getTime() > token.exp) {
      localStorage.removeItem(key);
      removeLocalStorage("user");
      return null;
    }
  } else if (key !== "user") {
    let parsedToken = Base64.parseJwt(token);
    if (now.getTime() > parsedToken.exp * 1000) {
      localStorage.removeItem(key);
      removeLocalStorage("user");
      return null;
    }
  }
  return token?.value ? token?.value : token;
}
