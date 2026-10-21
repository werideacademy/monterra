// Ridimensiona e comprime una foto per il web, rimuovendo i metadati EXIF/GPS.
// Uso: swift scripts/optimize.swift <input> <output.jpg> <lato_lungo_max> <qualita_0-1>
import Foundation
import ImageIO
import CoreGraphics
import UniformTypeIdentifiers

let a = CommandLine.arguments
let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!
let opts: [CFString: Any] = [
  kCGImageSourceCreateThumbnailFromImageAlways: true,
  kCGImageSourceCreateThumbnailWithTransform: true,
  kCGImageSourceThumbnailMaxPixelSize: Int(a[3])!,
]
let img = CGImageSourceCreateThumbnailAtIndex(src, 0, opts as CFDictionary)!
let srgb = CGColorSpace(name: CGColorSpace.sRGB)!
let ctx = CGContext(data: nil, width: img.width, height: img.height, bitsPerComponent: 8, bytesPerRow: 0,
                    space: srgb, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
ctx.interpolationQuality = .high
ctx.draw(img, in: CGRect(x: 0, y: 0, width: img.width, height: img.height))
let out = ctx.makeImage()!
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, out, [
  kCGImageDestinationLossyCompressionQuality: Double(a[4])!,
  kCGImagePropertyJFIFDictionary: [kCGImagePropertyJFIFIsProgressive: true],
] as CFDictionary)
CGImageDestinationFinalize(dst)
