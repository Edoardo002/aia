import router from "@/router";

export function start() {
  router.push({ path: '/login' })  }

export function sign() {
  router.push({ path: '/signup' })  }

export function dashboard(user) {
  router.push({ path: `/dashboard/${user.id}`});
}

export async function checkAuth(user_id) {
  const tokenStr = localStorage.getItem('token');
	if (!tokenStr) {
		return false;
	}
	const token = JSON.parse(tokenStr);
	const now = new Date();
	if (now.getTime() > token.expiry) {
		localStorage.removeItem(token);
		return false;
	}
  const response = await fetch('http://127.0.0.1:8000/chatbot/check', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ user_id:user_id, token:token.value })
  });
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    return true
  } else {
    const error = await response.json();
    console.error(error);
    return false
  }
}

export async function eLoginSubmit(name, last_name, email) {
  const response = await fetch('http://127.0.0.1:8000/chatbot/extlogin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ first_name:name, last_name:last_name, email:email })
  });
  if (response.ok) {
    const data = await response.json();
    console.log(data);
    const now = new Date();
    const token = {
      value: JSON.parse(data).token,
      expiry: now.getTime() + 3600*1000*4,
    }
    localStorage.setItem('token', JSON.stringify(token));
    dashboard(JSON.parse(data));
  } else {
    const error = await response.json();
    console.error(error);
    alert('Invalid e-mail or password');
  }
}