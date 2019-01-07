import json

plus  = lambda p,q : tuple(map(float, [p[i]+q[i] for i in range(3)]))
minus = lambda p,q : tuple(map(float, [p[i]-q[i] for i in range(3)]))
mult  = lambda p,f : tuple([float(p[i])*f for i in range(3)]) 

class ModelLoader:
    def __init__(self, path = "."):
        self.path = path
        self.db = {}

    def _resolveTexture(self, data, texname):
        if texname[0] != '#' : return texname
        if "textures" in data and texname[1:] in data["textures"]:
            return data["textures"][texname[1:]]
        return texname

    def _resolveElements(self, data):
        if "elements" in data:
            for ele in data["elements"]:
                for facename in ele["faces"]:
                    face = ele["faces"][facename]
                    face["texture"] = self._resolveTexture(data, face["texture"])
            return True
        return False

    def _resolveTextures(self, data):
        if "textures" in data:
            texs = data["textures"]
            for tex in texs:
                texs[tex] = self._resolveTexture(data, texs[tex])
            return True
        return False

    def _getModel(self, name): 
        with open(self.path + "/" + name + ".json", "r") as f:
            data = json.load(f)
        
        self._resolveElements(data)
            
        if "parent" in data and data["parent"] not in ["block/block", "block/thin_block"]:
            par_data = self._getModel(data["parent"])
            if "textures" in data:
                if "textures" not in par_data:
                    par_data["textures"] = {}
                for tex in data["textures"]:
                    par_data["textures"][tex] = data["textures"][tex]
            
            flag_eles = self._resolveElements(par_data)
            flag_texs = self._resolveTextures(par_data)
            if flag_eles or flag_texs: 
                return par_data
        return data

    def getModel(self, name):
        if name not in self.db:
            model = self._getModel(name)
            self.db[name] = model
            if "elements" in model:
                for ele in model["elements"]:
                    ele["from"] = mult(ele["from"], 1./16)
                    ele["to"] = mult(ele["to"], 1./16)
                    for facename in ele["faces"]:
                        face = ele["faces"][facename]
                        uv = [0., 0., 1., 1.]
                        if "uv" in face:
                            uv = list(face["uv"])
                            for i in range(4):
                                uv[i] /= 16.
                        # swap UV
                        uv = [uv[1], uv[0], uv[3], uv[2]]
                        # swap V
                        uv[0], uv[2] = uv[2], uv[0]
                        face["uv"] = tuple(uv)
        return self.db[name]
