Coiled/dask requires the local python environment to match the environment of the workers closely, so let's run this from a docker container:
docker run -p 8888:8888 ghcr.io/dask/dask-notebook  # the message gives the link to the jupyter server.

# The dask-notebook docker image doesn't have the coiled client by default!  No worries...
!pip install coiled


import coiled
cluster = coiled.Cluster(n_workers=2, worker_vm_types=["m7a.medium"],
     container="ghcr.io/dask/dask" )

client = cluster.get_client()


puzzle = ['b3068921221ef5440aac6fcc3ce044c3\n', 'cf2338821633c6a7badc5c99bf899291\n', '62fed3dddac9a364fb03bc32989df4c9\n', 'a485412c8970fdb93481946af88e436e\n', '29a0b76ded818a1d1b8431c2a9b481c9\n', 'bc0c62783a865f92be269befd24fa0c6\n', '134b532c447860e5628343706c141b21\n', '9fc00b57a902d292c51cd5fabbc5a3d6\n', '69e60ba95b38ad6a23fd5b1a902148d5\n', 'a77e84bf42c9fb0b1a4a7eccf8a912dc\n', '864560447a863eed9d608d42c25ddda4\n', '6f5f7b040e22ee5a27dfba0b1caeb2bc\n', 'a77e84bf42c9fb0b1a4a7eccf8a912dc\n', '0faf82e53a3487292e2bb496a24f9c1a\n', 'a36dff17f810ef1933047b81a926370f\n', 'a77e84bf42c9fb0b1a4a7eccf8a912dc\n', '06198703b797ad9e43b3e7d47e3a8ef4\n', 'df26711d31ab334175e194ffe1c0a368\n', '8fef7425f6ca0fda5ac6a93c130c47bc\n', '1d836a991e08b9f0be8fd3bab78da0d2\n', '0be0845104c8a77339242b71eec3831f\n', 'ceb23fa8834956ef4e4c7164e73f9f5c\n', '8ee6d268b9194d7d2c468564d5efaa45\n', '7a6a1a282f2ac3d9d2eca02fe24d9568\n', 'fbc536ba1ad0eaac2f4378b2e817a46a\n', '1baaf3f2dcac40bd0c88523db14777ee\n', '1d836a991e08b9f0be8fd3bab78da0d2\n', 'e969aa2641033fce4a3bed81b07c229c\n', 'de6fdd937530a838f41ea9e405cd6971\n', '2975d004a669f698f7d58c627a138a30\n', '4022bed40cb355a9a70cea32bb0b224f\n', '19e578025cdeebd6907d80803c58829f\n', 'e969aa2641033fce4a3bed81b07c229c\n', 'd3a14e38a34bac69cd054b950f73c9e1\n', 'cb90e97103237dbdcf7ce1727f720536\n', '035c49caec172c872784239752f171be\n', '6f5f7b040e22ee5a27dfba0b1caeb2bc\n', '0ef7391a01e158d5802f23f4704fa34a\n', 'c51b8baa9a83eedb719ac635ec6914c9\n', '14710d91c2e2423da10cf64e98e5dcb1\n', 'c529f1234d9ef5828402de95f1987639\n', '31e4f614fbe636b8e604e5dd47f6cddc\n', 'a77e84bf42c9fb0b1a4a7eccf8a912dc\n', 'aaf9233dca8a2f870bc868a5b6a215b6\n', 'f30620728e52fe734f32b3ee007f729a\n', '1d836a991e08b9f0be8fd3bab78da0d2\n', '672116272827359cf6fe07bae3d8ad39\n', 'ea12c590c8159c4e74e5d893827b9ee2\n']
puzzleeasy = ['d5f311f74b2490f29d030e74e380ff84\n', 'b4862fae46b2933db4ad08fc408c2621\n', 'fbf9100e94abb8d5697b077cd8a550bb\n', 'd4f8b83b938b82628ee164d39358ece4\n', '844a466c6bc4e01e9122baf2915399a3\n', 'f2bc49ad4f8b029dcde283aacbdc354a\n', 'b6f5d1e09710400ce651f63f4dfb9480\n', '258df4c64a2ca2ebc78f74045b56def8\n', '80c4414ccd9c3e6acf1e210be202d1ea\n', 'e37fb3e421c7cc7a3f1b10859670b879\n', '3b0ad9f48d16c9827ea62a02fbfd740b\n', 'bf2dbef4c8857792229ff5ac6ecfb39a\n', '94c6d3fc6259f9ea9e8e76426dc28409\n', 'ed878447d74db74fac133ee95f275d5f\n', 'dee07ce42fda9cbbda326ca937568e43\n', '249dafb8abcc4bb2847f8e0bf1a1a358\n', '785237ceed3e083d5f6538095f8d1343\n', '46b3d47cd894cd26ac96a3557f094fba\n', '995eb0d487641ae18d20241d356ad0c0\n', '43b410d5d092fa430f7f7be2af982b73\n', 'd27d0dec7141637282c7e36b0e91fb58\n', '341433318d6c1dcc3495ba6e9e12ff94\n', '207da583d9143938e0f1d5ff2b104029\n', '749a03d0f33a5e722faa9d30fca58819\n', 'b49f5c8808b9947e88c3d7446c7550b8\n', '8da3699474d0c0417a7bedfe6170c465\n', 'b6d9ca90b602c2c2e493a2cb76b2e66b\n', '9912c60fd48a3f4167773e0acdef2062\n', 'bfaf43058084faf29ec65ec9ce195a19\n', 'e37fb3e421c7cc7a3f1b10859670b879\n', '1add2d980058404aae5a72d371e483f2\n']
puzzlehard = ['3193d730fcda5a16fc9f1dba9242df02\n', '8ffb79046f652b47113dc0569d9b43bf\n', '5e4d40162dd7516d515b4c841280752b\n', 'e9e8ae9eb90e8ae813a8e1e0689b5343\n', 'af1ce2fb1c59c16223b35bbb29b0674d\n', '9aff5d7cc4138fdef6606c04b8017d8f\n', 'cfb3af10201c69dffe878772f49cca6a\n', 'c6d94ddc87b785426ea839a2c3e29238\n', '0644d5ab81ec149422fdbfe36eb9a78d\n', '646a53576f23b157d94a7f61faf4a780\n', 'eeb469b0520546cd520c603f376672eb\n', '3c7ef35acbe6f2cbd00131f98bba9899\n', '13bffc4ea22a6b9484eb73d9d2f0040c\n', 'fcaa84ecfa78b9282a14cd11502acf34\n', 'b09c2fb96aa341b417b057fb35a00a74\n', '9aff5d7cc4138fdef6606c04b8017d8f\n', '75b8385746264408f1d9d531bc1c72e3\n', 'cea168f661650df399b3b9883312698a\n', 'e9e8ae9eb90e8ae813a8e1e0689b5343\n', '005c10d4338d5d3a3fcf806930d81275\n', '3e2da7fead198c904e45219e1b94718e\n', '0184dafed0e7924d2e7f70c0a2ff7d4c\n', '12e5b8ca1413b5651044fa6607cd268e\n', '8a83e9aca8b0062ad5d1d040514570b0\n', '9aff5d7cc4138fdef6606c04b8017d8f\n', '75b8385746264408f1d9d531bc1c72e3\n', '57e35526fa00b381bfb1c48faa1661b1\n', '75b8385746264408f1d9d531bc1c72e3\n', '0c4b3328b210388b51e32660906c90dc\n', 'a378b7e79d377257ec5462a6e7bfc7da\n', 'fac358274be0f68e496dc652d732f5b6\n', '8f9a896fddd8c5410c548f50c9274448\n', 'fe634c78e80ab4b08eaf9888cbc48aa8\n', '75b8385746264408f1d9d531bc1c72e3\n', 'd831be31e7b994460930d1821c791c49\n', '488d831afc8482f5b3f6465ccb063892\n', 'a378b7e79d377257ec5462a6e7bfc7da\n', '60576249c0396adbf06446cea1412521\n', '4e90989aa688f16355b3f1d0cec90d17\n', '15be8a3d34f26cd8de0a98f0029e5137\n', '9aff5d7cc4138fdef6606c04b8017d8f\n', '7ee5d9ac38712f04690460e89fcee569\n', '96707e35d58255adde5f8b54b4dcd6a8\n', '84c959d92ffdf2e25325a7f2f3ec19e7\n', '7addc7cf63499da2c573a425e0f4a5ae\n', 'ca5752c4941cb5d367d91ef976780c1c\n', '9aff5d7cc4138fdef6606c04b8017d8f\n', '75b8385746264408f1d9d531bc1c72e3\n', '08373d5bc2bed775389f7cfc8693acd9\n', '2ae58da1dd8d4a2279659ab926c173d9\n', 'a378b7e79d377257ec5462a6e7bfc7da\n', '57896733d7893596eb56b2c239680de1\n', 'ff0e18802910faeb8922b6b53bf177ca\n', '83d502467e427db8bb4f935c05ec37a3\n', '214e0dba04924199e5a945fb99732e44\n', '8da13efa2c4fd7b4367922db10c47ba0\n', 'bfe238f67dcfc9e573bdbadf41043dcc\n', '299e4c67d97d935067295421329eb769\n', 'e78043f2951499bbfd08a3f5a7a5a45c\n', '57896733d7893596eb56b2c239680de1\n', '272fcaae279b0b58eacc28dbe688b8a4\n', '5fe9b5241b71d7a8dc57be170e8a6f30\n', 'c18facf063ed69b421e9a34be009f3c6\n', '545de004baf44cadf150dde0929df989\n', '40cc44ebcd4226f6174daff874b33cf2\n', '83d502467e427db8bb4f935c05ec37a3\n', '57896733d7893596eb56b2c239680de1\n', '007b16546c01c3f3ca01e8733b11de30\n', '299e4c67d97d935067295421329eb769\n', '538eeb2e4dafe82d94e1702c4616ff72\n', '979cefd71ae4aa96beefc04ea6c0e971\n', '75b8385746264408f1d9d531bc1c72e3\n', 'afe21a992da09dd69f43d9c754fad751\n', 'fd6143e42aace102774d81d618d46298\n', '83d502467e427db8bb4f935c05ec37a3\n', '4bf6342c9fe2031f3640de761ef514bb\n', '077d275863b24f808384ce1170f8b84d\n', '9aff5d7cc4138fdef6606c04b8017d8f\n', '82cd0bfc47ae384a9a0b749ff41052a5\n', '83d502467e427db8bb4f935c05ec37a3\n', '75b8385746264408f1d9d531bc1c72e3\n', '1ecc482e4a815fb69b98dc779aeb03d8\n', 'a378b7e79d377257ec5462a6e7bfc7da\n', 'b9f617e9a002a907d700dadbc53c4219\n', 'e92b5937cd45d1ee054caa5e52e15642\n', '84c959d92ffdf2e25325a7f2f3ec19e7\n', 'e58942213073a83855083165433d4141\n', 'e7fdf949b50a6d7f0d0f0454b69db040\n', '8476cd9d2eea284fd42048f4a07dea79\n', '299e4c67d97d935067295421329eb769\n', 'ebb6a6736ac07a24870df779fb89c0ac\n', '1d04c4e6bf42c437c719fc85f488d6b5\n']

p = [puz.strip() for puz in puzzle]
#p = [puz.strip() for puz in puzzleeasy]

pset = set(p)


import hashlib
import dask.bag as db
import datetime

wordlist = ["the","The"]
N = 200

tgts = range(N)


def check_hash(j):
    for i in range(j*5000000, (j+1)*5000000):
 #       key = "{:09d}".format(i)
        key = "{:09d}".format(i)

        for word in wordlist:
            hash = hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
            if hash in pset:
                return (hash, key, word)
    return None


def main():
    bag = db.from_sequence(tgts, npartitions=20)  # Adjust npartitions for your system
    results = bag.map(check_hash).filter(lambda x: x is not None).compute()

    # Print results
    for result in results:
        print(result)


start = datetime.datetime.now()
main()
print(datetime.datetime.now()-start)



# https://cloud.coiled.io/clusters

