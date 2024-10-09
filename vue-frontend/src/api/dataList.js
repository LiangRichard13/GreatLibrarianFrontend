import service from "@/utils/request";

export function getDataList(data) {
    return service({
        url: '/datasets',
        method: 'post',
        data:data
    })
}