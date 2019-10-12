import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate
import maya.cmds as cmds
 
class AEaiLayerProbabilityTemplate(ShaderAETemplate):
	def EnableLayerChange(self,plugName):
		enabledAttr = '{}.{}'.format(self.nodeName, plugName)
		dimLayer = (cmds.getAttr(enabledAttr) == 0)
		dimLayerInverse = (cmds.getAttr(enabledAttr) == 1)
		getMelaninStatus = '{}.{}'.format(self.nodeName, plugName.replace('Layer ', 'outputMelanin_L'))
		dimLayer_global = (cmds.getAttr(getMelaninStatus) ==0)
		dimLayerInverse_global= (cmds.getAttr(getMelaninStatus) ==1)
		#if plugName[0:13]=='outputMelanin':
		#	enabledAttr_melanin = '{}.{}'.format(self.nodeName, plugName)
		#	dimLayer_global = (cmds.getAttr(enabledAttr_melanin)==0)
		#	dimLayerInverse_global = (cmds.getAttr(enabledAttr_melanin)==1)
		

		if plugName[0:13]=='outputMelanin':
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('outputMelanin_', 'melaninRoot_'), dimLayer ))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('outputMelanin_', 'melaninTip_'), dimLayer ))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('outputMelanin_', 'rootColor_'), dimLayerInverse ))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('outputMelanin_', 'tipColor_'), dimLayerInverse ))
		else:
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'outputMelanin_L'), dimLayer ))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'melaninRoot_L'), dimLayer_global if(dimLayerInverse==True) else dimLayer))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'melaninTip_L'), dimLayer_global if(dimLayerInverse==True) else dimLayer))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'rootColor_L'), dimLayerInverse_global if(dimLayerInverse==True) else dimLayer))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'tipColor_L'), dimLayerInverse_global if(dimLayerInverse==True) else dimLayer))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'probability_L'), dimLayer ))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'pos_L'), dimLayer ))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'soft_L'), dimLayer ))
			cmds.editorTemplate(dimControl=(self.nodeName, plugName.replace('Layer ', 'posDir_L'), dimLayer ))

	def setup(self):
		# Add the shader swatch to the AE
		self.addSwatch()
		self.beginScrollLayout()
 
		# Add a list that allows to replace the shader for other one
		self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')
		
		self.addControl('randInput', label='randomInput', annotation='utility random input')
		self.beginLayout("Barycentric coordinates", collapse=False)
		self.addControl('Barycentric', label='Enable', annotation='use barycentric coordinates (for IGS hairs)')
		self.addControl('BarycentricU', label='Ucoord', annotation='Barycentric U coordinate')
		self.addControl('BarycentricV', label='Vcoord', annotation='Barycentric V coordinate')
		self.endLayout()
		#--------------------------------------------------------------------------------------------------
		
		self.beginLayout("Base Color", collapse=False)
		enableAttr='outputMelanin_'+'BC'
		self.addControl(enableAttr, label='use Melanin', annotation='use melanin for'+'base layer',  changeCommand=lambda arg=None, x=enableAttr: self.EnableLayerChange(x))
		#self.addControl('outputMelanin_BC', label='use Melanin', annotation='Enable melanin ouput')
		self.addControl('melaninRoot_BC', label='root melanin', annotation='melanin root color')
		self.addControl('melaninTip_BC', label='tip melanin', annotation='melanin tip color')
		self.addSeparator()
		self.addSeparator()
		self.addControl('rootColor_BC', label='root color', annotation='custom root color')
		self.addControl('tipColor_BC', label='tip color', annotation='custom tip color')
		self.addSeparator()
		self.addSeparator()
		self.addControl('pos_BC', label='position', annotation='color position')
		self.addControl('soft_BC', label='softness', annotation='postion softness')
		self.addControl('posDir_BC', label='direction', annotation='root to tip, tip to root')
		self.endLayout()
		
		for i in range(1, 11):
			#self.EnableLayerChange('outputMelanin_'+'L{}'.format(i))
			self.beginLayout('Layer {}'.format(i), collapse = (i > 1))
			enableAttr_L = 'Layer {}'.format(i)
			self.addControl(enableAttr_L, label='Enable', annotation='Enable'+'layer {}'.format(i),  changeCommand=lambda arg=None, y=enableAttr_L: self.EnableLayerChange(y))
			#self.addControl('Layer {}'.format(i), label='Enable', annotation='Enable'+('Layer {}'.format(i)))
			enableAttr='outputMelanin_'+'L{}'.format(i)
			self.addControl(enableAttr, label='use Melanin', annotation='use melanin for'+'layer {}'.format(i),  changeCommand=lambda arg=None, x=enableAttr: self.EnableLayerChange(x))
			#self.addControl('outputMelanin_'+'L{}'.format(i), label='Enable', annotation='use melanin for'+'layer {}'.format(i))
			self.addControl('melaninRoot_'+'L{}'.format(i), label='root melanin', annotation='melanin root color')
			self.addControl('melaninTip_'+'L{}'.format(i), label='tip melanin', annotation='melanin tip color')
			self.addSeparator()
			self.addSeparator()

			self.addControl('rootColor_'+'L{}'.format(i), label='root color', annotation='custom root color')
			self.addControl('tipColor_'+'L{}'.format(i), label='tip color', annotation='custom tip color')
			self.addSeparator()
			self.addSeparator()
		
			self.addControl('probability_'+'L{}'.format(i), label='probability', annotation='probability of Layer '+str(i))
			self.addControl('pos_'+'L{}'.format(i), label='position', annotation='position of Layer '+str(i))
			self.addControl('soft_'+'L{}'.format(i), label='softness', annotation='softness of Layer '+str(i)+' position')
			self.addControl('posDir_'+'L{}'.format(i), label='direction', annotation='root to tip, tip to root')
			self.endLayout()
		
		# include/call base class/node attributes
		pm.mel.AEdependNodeTemplate(self.nodeName)
 
		# Add Section for the extra controls not displayed before
		self.addExtraControls()
		self.endScrollLayout()