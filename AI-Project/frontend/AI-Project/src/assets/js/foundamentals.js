import router from "@/router";

export function start() {
  router.push({ path: '/login' })  }

export function sign() {
  router.push({ path: '/signup' })  }

export function dashboard(user) {
  router.push({ path: `/dashboard/${user.id}`});
}

export async function checkAuth(user_id) {
  const response = await fetch('http://127.0.0.1:8000/chatbot/check', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ user_id:user_id })
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