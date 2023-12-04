import service from "@/utils/request";

export function findByUserId(id) {
    return service({
        url: '/apiConfig/findByUserId/'+id,
        method: 'get',
    })
}
export function deleteById(id) {
    return service({
        url: '/apiConfig/deleteById/'+id,
        method: 'delete',
    })
}

export function addApiKey(data) {
    return service({
        url: '/apiConfig/addApiKey',
        method: 'post',
        data: data
    })
}