import service from "@/utils/request";

export function findById(id) {
    return service({
        url: 'user/findById',
        method: 'get',
        data:id
    })

}

export function Login(data) {
    return service({
        url: 'user/login',
        method: 'post',
        data: data
    })
}

export function Register(data){
    return service({
        url: 'user/register',
        method: 'post',
        data: data
    })
}