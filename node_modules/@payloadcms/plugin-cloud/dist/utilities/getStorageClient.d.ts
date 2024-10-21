import * as AWS from '@aws-sdk/client-s3';
export type GetStorageClient = () => Promise<{
    identityID: string;
    storageClient: AWS.S3;
}>;
export declare const getStorageClient: GetStorageClient;
//# sourceMappingURL=getStorageClient.d.ts.map