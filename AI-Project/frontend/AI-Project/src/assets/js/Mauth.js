import '@/assets/js/auth/msal-browser.min.js';
import { eLoginSubmit } from '@/assets/js/foundamentals';

const msalConfig = {
    auth: {
        clientId: 'aca7234f-2dde-45a9-9eef-06d5e649444a',
        redirectUri: 'http://localhost:5173/login',
    }
};

const msalInstance = new msal.PublicClientApplication(msalConfig);

export async function signIn() {
    try {
        const loginResponse = await msalInstance.loginPopup({
            scopes: ["user.read"]
        });
        console.log(loginResponse);
        mCallback(loginResponse.account);
    } catch (error) {
        console.error(error);
    }
}

export function signOut() {
    msalInstance.logoutPopup().then(() => {
        //
    }).catch((error) => {
        console.error(error);
    });
}

function mCallback(response) {
    const account = JSON.parse(JSON.stringify(response));
    eLoginSubmit(account.name, "mAuth", account.username);
}