import service from "@/utils/request";

export function getDataList(data) {
    return service({
        url: '/datasets',
        method: 'get',
        data:data
    })
}