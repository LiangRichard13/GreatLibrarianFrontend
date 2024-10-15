import service from "@/utils/request";

export function getDataList(data) {
    return service({
        url: '/datasets',
        method: 'post',
        data:data
    })
}

export function buildTest(data) {
    return service({
        url: '/datasets/testset_build',
        method: 'post',
        data:data
    })
}