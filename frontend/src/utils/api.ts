import router from "@/router";
import request from "./request";


function logout(needRequest: boolean = true) {  
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    
    if (token && username && needRequest) {
        request.get('/account/logout', {
            params: {
                username,
                token
            }
        }).then(() => {
            router.push('/login');
        }).catch(() => {
            router.push('/login');
        });
    } else {
        router.push('/login');
    }

    localStorage.removeItem('token');
    localStorage.removeItem('username');
}

async function changePassword(newpassword: string, oldpassword: string) {
    try {
        const res = await request.post('/account/change-password', {
            newpassword,
            oldpassword
        });
        return res.data;
    } catch (error) {
        return error;
    }
}

async function getProfile(username?: string) {
    try {
        const res = await request.get('/account', {
            params: {
                name: username || localStorage.getItem('username')
            }
        });
        return res.data;
    } catch (error) {
        return error;
    }
}

async function updateProfile(data: {
    username: string;
    newname?: string;
    email?: string;
    phone?: string;
}) {
    try {
        const res = await request.patch('/account', data);
        return res.data;
    } catch (error) {
        return error;
    }
}


async function getClasses(data: {
    id?: string;
    cls?: string;
}) {
    try {
        const res = await request.get('/class', {
            params: data
        });
        return res.data;
    } catch (error) {
        return error;
    }
}

async function getEvaluations(data: {
    id?: string;
    class_id?: string;
    student_id?: string;
    class_name?: string;
    student_name?: string;
}) {
    try {
        if (data.student_name !== undefined) {
            const user_res = await getProfile(data.student_name);
            if (!user_res.success) {
                return user_res;
            }
            data.student_id = user_res.data.id;
        }

        if (data.class_name) {
            const cls_res = await getClasses({cls: data.class_name});
            if (!cls_res.success) {
                return cls_res;
            }
            data.class_id = cls_res.data.id;
        }

    
        const res = await request.get('/evaluation', {
            params: {
                id: data.id,
                cls: data.class_id,
                user: data.student_id
            }
        });
        return res.data;
    } catch (error) {
        return error;
    }
}


export default {
    logout,
    changePassword,
    getProfile,
    updateProfile,
    getClasses,
    getEvaluations
}