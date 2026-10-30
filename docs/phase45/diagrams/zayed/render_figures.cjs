const path=require('path'),fs=require('fs');
const packages=process.env.DAWRA_NODE_MODULES;
const sharp=require(packages?path.join(packages,'sharp'):'sharp');
const images=path.resolve(__dirname,'../../images');
(async()=>{
 for(const name of fs.readdirSync(images).filter(n=>/^figure-9-.*-part-[12]\.svg$/.test(n))){
  const activity=name.includes('activity');
  const rendered=await sharp(path.join(images,name),{density:activity?96:190}).png().toBuffer();
  const target=path.join(images,name.replace('.svg','.png'));
  fs.writeFileSync(target+'.tmp',rendered);
  fs.renameSync(target+'.tmp',target);
 }
 console.log('Rendered 12 PNG print parts.');
})().catch(e=>{console.error(e);process.exit(1)});
