import service from "@/utils/request";

export function findById(data) {
    return service({
        url: '/user/findById',
        method: 'post',
        data:data
    })

}

export function Login(data) {
    return service({
        url: '/user/login',
        method: 'post',
        data: data
    })
}

export function Register(data){
    return service({
        url: '/user/register',
        method: 'post',
        data: data
    })
}

export function isExpired(data){
    return service({
        url: '/user/isExpired',
        method: 'post',
        data: data
    })
}