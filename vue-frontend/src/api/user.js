import service from "@/utils/request";

export function findById(id) {
    return service({
        url: '/user/findById',
        method: 'post',
        data:id
    })

}

export function Login(data) {
    return service({
        url: '/user/login',
        method: 'post',
        data: data
    })
}

export function Register(data) {
    return service({
        url: '/user/register',
        method: 'post',
        data: data
    })
}

export function isExpired(token) {
    return service({
        url: '/user/isExpired',
        method: 'post',
        data:token
    })
}

export function updateUser(data) {
    return service({
        url: '/user/update',
        method: 'post',
        data: data
    })
}

export function editPassword(data) {
    return service({
        url: '/user/editPassword',
        method: 'post',
        data: data
    })
}

export function uploadAvatar(data,uid) {
    return service({
        url: "/user/icon",
        method: 'post',
        data: data,
        params:{
            uid:uid
        },
        headers: {
            'Content-Type': 'multipart/form-data'
          },
    })
}

export function getUserIconUrl(data) {
    return service({
        url: "/user/icon",
        method: 'get',
        data: data,
    })
}

export function removeUserIp(id) {
    return service({
            url: "/user/loginOut",
            method: 'put',
            params:{
                uid:id
            }
        }
    )
    }

    export function setUserIp(id) {
        return service({
            url: "/user/setUserIp",
            method: 'put',
            params:{
                id:id
            }
        })

    }