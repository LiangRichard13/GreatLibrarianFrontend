import service from "@/utils/request";

export function findById(id) {
    return service({
        url: '/user/findById',
        method: 'get',
        params: {
            id: id
        }
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
        method: 'get',
        params: {
            loginToken: token
        }
    })
}

export function updateUser(data) {
    return service({
        url: '/user/updateUser',
        method: 'put',
        data: data
    })
}

export function uploadAvatar(data) {
    return service({
        url: "/upload",
        method: 'post',
        data: data,
        headers: {
            'Content-Type': 'multipart/form-data'
          },
    })
}

export function removeUserIp(id) {
    return service({
            url: "/user/removeUserIp",
            method: 'delete',
            params:{
                id:id
            }
        }
    )
    }

    export function setUserIp(data) {
        return service({
            url: "/user/setUserIp",
            method: 'post',
            data: data
        })

    }