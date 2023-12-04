import service from "@/utils/request";

export function findByUserId(id) {
    return service({
        url: '/dataSetConfig/findByUserId/'+id,
        method: 'get',
    })
}
export function deleteById(id) {
    return service({
        url: '/dataSetConfig/deleteById/'+id,
        method: 'delete',
    })
}

export function addDateSet(data) {
    return service({
        url: '/dataSetConfig/addApiKey',
        method: 'post',
        data: data
    })
}