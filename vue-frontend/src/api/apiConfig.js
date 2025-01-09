import service from "@/utils/request";

export function findApiKeyByUserId(id) {
    return service({
        url: '/APIKey',
        method: 'get',
        params: {
            uid: id
        }
    })
}

export function deleteById(data) {
    return service({
        url: '/APIKey',
        method: 'delete',
        data:data
    })
}

export function addApiKey(data) {
    return service({
        url: '/APIKey',
        method: 'post',
        data: data
    })
}

export function addCallFunction(id,code) {
    return service({
        url: '/APIKey',
        method: 'put',
        data: {
            choose:"1",
            id:id,
            code:code
        }
    })
}

export function getCallFunction(id) {
    return service({
        url: '/APIKey',
        method: 'put',
        data: {choose:"2",id:id}
    })
}


export function testConnectivity(value,code,retries) {
    return service({
        url: '/APIKey',
        method: 'put',
        data: {choose:"3",value:value,code:code,retries:retries}
    })
}